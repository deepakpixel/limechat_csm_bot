require('dotenv').config();
const express = require('express');
const account = require('./models/account');
const ticket = require('./models/ticket');
const user = require('./models/user');
const app = express();
const axios = require('axios');
const mongoose = require('mongoose');
app.set('view engine', 'ejs');

app.use(express.json());
app.use(express.urlencoded({ extended: false }));

app.use((req, res, next) => {
  console.log('BODY: ', req.body);
  // if (req.headers['Authorization'] !== process.env.AUTH_SECRET)
  //   return res.status(401).json();
  next();
});

app.post('/create-ticket', async (req, res) => {
  console.log('Start- Create Ticket');
  try {
    let title = req.body.title;
    let description = title;
    let reporter = req.body.contact_id;

    if (!title || !reporter) throw Error('No title or reporter');
    let type = title.split(':')[0].toLowerCase();

    let acc = await account.findOne({ contact: reporter });
    if (!acc) throw Error('No account details for this user');

    if (['bug', 'doubt', 'request'].indexOf(type) == -1)
      return res.json({
        sendMessages: [
          {
            username: acc.contact,
            content:
              'Invalid query type, please raise the query in format "BUG: This is the bug"',
          },
          {
            username: acc.contact,
            content: 'We support query type as *BUG*, *REQUEST*, *DOUBT*',
          },
        ],
      });

    if (title.length > process.env.MAX_TITLE_LENGTH)
      title = title.substring(0, process.env.MAX_TITLE_LENGTH) + '...';

    title = title.split(':');
    title.shift();
    title = title.join(':').trim();

    // tick = await ticket.create({
    //   title,
    //   description,
    //   reporter,
    //   type,
    // });

    tick = await axios.post(
      'https://api.clickup.com/api/v2/list/181298135/task',
      {
        name: title,
        description: description,
        status: 0,
        start_date_time: false,
        notify_all: true,
        parent: null,
        links_to: null,
        tags: [type],
      },
      {
        headers: {
          Authorization: process.env.CLICKUP_PERSONAL_TOKEN,
        },
      }
    );
    tick = tick.data;
    return res.json({
      sendMessages: [
        {
          username: acc.contact,
          content:
            'Your ticket has been created\\. Our CSM Team is looking into it you should get the update on it in next few hours\\.',
        },
        // {
        //   username: acc.csm,
        //   content: `Hi, A new ticket is created by ${reporter} for client ${acc.name}\\. Please check this for more details [http://localhost:3333/tickets/${tick.id}](http://127.0.0.1:3000/tickets/${tick.id})`,
        // },
        {
          username: acc.csm,
          content: `Hi, A new ticket is created by ${reporter} for client ${acc.name}\\. Please visit this link for more details [https://sharing\\.clickup\\.com/37432238/v/6\\-181298135\\-1/t/h/${tick.id}/2b734658e130b6f](https://sharing.clickup.com/37432238/v/6-181298135-1/t/h/${tick.id}/2b734658e130b6f)`,
        },
      ],
    });
  } catch (err) {
    console.log(err);
    return res.status(500).json({ err: err.message });
  }
});

app.get('/tickets/:id', async (req, res) => {
  id = req.params.id;
  console.log(id);
  tick = await ticket.findById(id);
  if (tick) return res.render('ticket', { tick });
  else return res.sendStatus(404);
});

app.use((req, res, next) => {
  console.log('Not found');
  return res.status(404).json({});
});
app.use((err, req, res, next) => {
  console.log('Express error handler, ERR', err.message);
  return res.status(500).json({ err: err.message });
});

PORT = process.env.PORT;

// Connect Mongo
mongoose.connect(
  'mongodb://127.0.0.1:27017/csm',
  {
    useUnifiedTopology: true,
    useNewUrlParser: true,
  },
  (err) => {
    if (!err) console.log('MONGO CONNECTED');
    app.listen(PORT, () =>
      console.log(`Server is up and running 🚀 on port ${PORT}`)
    );
  }
);

mongoose.connection.on('error', (err) => {
  // CRITICAL MONGO ERROR
  console.log('MONGO connection error: ', err);
});

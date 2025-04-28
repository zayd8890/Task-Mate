const router = require('express').Router()
const {google} = require('googleapis')
const CLIENT_ID = '646982956982-eiahoitalcloqgg6a23bsjb4da32auf0.apps.googleusercontent.com'
const CLIENT_SECRET = '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' 
//const REFRESH_TOKEN = '1//0gk2r7v4x3c5BCgYIARAAGAkSNwF-L9IrX6Z8aJm2bqj0d1fWz4e7h8nq3l5G6QKxXkVt9i1s4v2p0c3u7H5gYw'

const oauth2Client = new google.auth.OAuth2(
  CLIENT_ID,
  CLIENT_SECRET,
  REDIRECT_URI = 'http://localhost:3000'
)
router.get('/', async (req, res, next) => {
  res.send({ message: 'Ok api is working 🚀' });
});
router.post('/create-tokens', async (req, res, next) => {
  try{
    const { code } = req.body
    const { tokens } = await oauth2Client.getToken(code)
    res.send(tokens)
  } catch(error){
    next(error)
  }
})


router.post('/create-event', async (req, res, next) => {
  try{
    const { summary, description, location, startDateTime, endDateTime } = 
    req.body

    oauth2Client.setCredentials({refresh_token: tokens})
    const calendar = google.calendar({ version: 'v3' })
    const response = await calendar.events.insert({
      auth: oauth2Client,
      calendarId: 'primary',
      //timeMin: (new Date()).toISOString(),
      //maxResults: 10,
      //singleEvents: true,
      //orderBy: 'startTime',
      requestBody: {
        summary,
        description,
        location,
        colorId: '1',
        start: {
          dateTime: new Date(startDateTime),
          timeZone: 'America/Los_Angeles',
        },
        end: {
          dateTime: new Date(endDateTime),
          timeZone: 'America/Los_Angeles',
        },
      },
    })
    
      res.send(response)
  
  }catch(error){
    next(error)
  }
})

module.exports = router;

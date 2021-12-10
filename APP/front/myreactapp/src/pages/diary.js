import * as React from 'react';
import AppBar from '@mui/material/AppBar';
import Button from '@mui/material/Button';
import NoteIcon from '@mui/icons-material/Note';
import CssBaseline from '@mui/material/CssBaseline';
import Stack from '@mui/material/Stack';
import Box from '@mui/material/Box';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import Container from '@mui/material/Container';
import Link from '@mui/material/Link';
import useRecorder from "../useRecorder";

import { createTheme, ThemeProvider } from '@mui/material/styles';

function Copyright() {
    return (
      <Typography variant="body2" color="text.secondary" align="center">
        {'Copyright © '}
        <Link color="inherit" href="https://mui.com/">
          Your Website
        </Link>{' '}
        {new Date().getFullYear()}
        {'.'}
      </Typography>
    );
}

const theme = createTheme({
    palette: {
      primary: {
        main: "#006400"
      },
      secondary: {
        main: "#ffa500"
      }
    }
}); 

const Diary = function() {
    let [audioURL, isRecording, returnValue, startRecording, stopRecording] = useRecorder(false);

    return (
        <ThemeProvider theme={theme}>
          <CssBaseline />
          <AppBar position="relative" color="primary">
            <Toolbar>
              <NoteIcon sx={{ mr: 2 }} />
              <Typography style={{ marginRight: 16 }} variant="h6" color="inherit" onClick={event =>  window.location.href='/'}>
                Home Page
              </Typography>
              <Typography style={{ marginRight: 16 }} variant="h6" color="inherit" onClick={event =>  window.location.href='/register'}>
                Register
              </Typography>
              <Typography style={{ marginRight: 16 }} variant="h6" color="inherit" onClick={event =>  window.location.href='/diary'}>
                Diary
              </Typography>
            </Toolbar>
          </AppBar>
          <main>
            {/* Hero unit */}
            <Box
              sx={{
                bgcolor: 'background.paper',
                pt: 8,
                pb: 6,
              }}
            >
              <Container maxWidth="sm">
                <Typography
                  component="h1"
                  variant="h2"
                  align="center"
                  color="text.primary"
                  gutterBottom
                >
                  Diary
                </Typography>

                <div style={{ display: 'flex',  justifyContent:'center', alignItems:'center' }}>
                    <audio src={audioURL} controls style={{marginRight: '0px', display: 'block'}}></audio>
                </div>

                <Stack
                  sx={{ pt: 4 }}
                  direction="row"
                  spacing={2}
                  justifyContent="center"
                >
                  <Button variant="contained" onClick={startRecording} disabled={isRecording}>Record</Button>
                  <Button variant="outlined" onClick={stopRecording} disabled={!isRecording}>Stop</Button>
                </Stack>
              </Container>
            </Box>
            <Container sx={{ py: 8 }} maxWidth="md">
              {/* End hero unit */}

              <Typography variant="h6" align="center" gutterBottom>
              {'detected emotion : ' + returnValue.emotion}
              </Typography>

              <Typography variant="h6" align="center" gutterBottom>
              {returnValue.text}
              </Typography>
              
            </Container>
          </main>
          {/* Footer */}
          <Box sx={{ bgcolor: 'background.paper', p: 6 }} component="footer">
            <Typography variant="h6" align="center" gutterBottom>
              Footer
            </Typography>
            <Typography
              variant="subtitle1"
              align="center"
              color="text.secondary"
              component="p"
            >
              Something here to give the footer a purpose!
            </Typography>
            <Copyright />
          </Box>
          {/* End footer */}
        </ThemeProvider>
    )
}

export default Diary;
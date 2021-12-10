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

const Homepage = function() {

    return (
        <ThemeProvider theme={theme}>
          <CssBaseline />
          <AppBar position="relative" >
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
                  One-line Emotion Diary
                </Typography>
                <Typography variant="h5" align="center" color="text.secondary" paragraph>
                  {/* Something short and leading about the collection below—its contents,
                  the creator, etc. Make it short and sweet, but not too short so folks
                  don&apos;t simply skip over it entirely. */}
                  Register your self with your voice, and record your daily Emotion with a short voice comment!

                </Typography>
                <Stack
                  sx={{ pt: 4 }}
                  direction="row"
                  spacing={2}
                  justifyContent="center"
                >
                  <Button variant="contained" onClick={event =>  window.location.href='/register'}>Register</Button>
                  <Button variant="outlined" onClick={event =>  window.location.href='/diary'}>Diary</Button>
                </Stack>
              </Container>
            </Box>
            <Container sx={{ py: 8 }} maxWidth="md">
              {/* End hero unit */}
              
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
      );
  
}

export default Homepage;

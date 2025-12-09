import '@mantine/core/styles.css';

import { MantineProvider } from '@mantine/core';
import { Router } from './Router.js';
import { theme } from './theme.js';
import StepBar from './components/StepBar.js';
import Home from './pages/Home.js';

export default function App() {
  return (
    <MantineProvider theme={theme}>
      <Home />
    </MantineProvider>
  );
}

// App.tsx
import React from 'react';
import { ThemeProvider } from './components/ThemeContext';
import Chatbot from './components/ChatBot';

function App() {
  return (
    <ThemeProvider>
      
      <Chatbot />
    </ThemeProvider>
  );
}

export default App;

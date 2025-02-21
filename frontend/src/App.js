import React, { useState } from 'react';
import { ChatProvider } from './components/ChatContext';
import ChatWindow from './components/ChatWindow';
import Sidebar from './components/Sidebar';
import StartupPage from './components/StartupPage'; // Renaming LoginPage to StartupPage
import './App.css';

function App() {
  const [hasStarted, setHasStarted] = useState(false);

  const handleStart = () => {
    setHasStarted(true);
  };

  return (
    <ChatProvider>
      <div className="App">
        <header className="app-header">
          <h1>Chat Application</h1>
        </header>

        <div className="main-content">
          {hasStarted ? (
            // Render the main chat window and sidebar after starting
            <>
              <Sidebar />
              <ChatWindow />
            </>
          ) : (
            // Show the startup page when not started
            <StartupPage onStart={handleStart} />
          )}
        </div>
      </div>
    </ChatProvider>
  );
}

export default App;

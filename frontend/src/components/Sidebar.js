import React, { useState, useEffect } from 'react';
import { useChat } from './ChatContext'
import './Sidebar.css';
import DropdownButton from './DropdownButton'; 


//Makes a sidebar with dropdown options from dropdown button
const Sidebar = () => {
  const { setMessages } = useChat(); 
  const [selectedOption1, setSelectedOption1] = useState("OpenAI");
  const [selectedOption2, setSelectedOption2] = useState("Select Your Model");
  const dropdown2Options = selectedOption1 === "OpenAI"
  ? ["GPT-4o", "GPT-4o-mini", "o1", "o1-mini"]
  : selectedOption1 === "Anthropic"
  ? ["Claude 3.5 Sonnet", "Claude 3.5 Haiku"]
  : [];

//When the dropdown for OpenAI or Anthropic is changed, reset the second dropdown to default value
  useEffect(() => {
    setSelectedOption2("Select Your Model");

  }, [selectedOption1]);


// When you hit the 2nd dropdown and choose a model, send a request to the flask
// server to change llms to the respective model.
  useEffect(() => {
    if (selectedOption2 !== "Select Your Model") {
//This part resets the chat when you select a different model
      setMessages([]);  
      fetch('http://localhost:5000/api/change_model', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          service: selectedOption1,
          model: selectedOption2,
        }),
      })
      .then(response => response.json())
      .then(data => {
        console.log('Model change successful', data);
      })
      .catch(error => {
        console.error('Error changing model:', error);
      });
    }
  }, [selectedOption2]);

  return (
    <div className="sidebar">
      <h2>Choose Your Model</h2>

      {/* Dropdown 1 */}
      <DropdownButton
        label="Dropdown 1"
        options={["OpenAI", "Anthropic"]}
        selectedOption={selectedOption1}
        onSelect={setSelectedOption1}
      />

      {/* Dropdown 2 */}
      <DropdownButton
        label="Dropdown 2"
        options={dropdown2Options}
        selectedOption={selectedOption2}
        onSelect={setSelectedOption2}
      />
    </div>
  );
};

export default Sidebar;

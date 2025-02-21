import React from 'react';
import './DropdownButton.css'; 


//Creates a button to be used in the dropdowns
const DropdownButton = ({ label, options, selectedOption, onSelect }) => {
  const [isOpen, setIsOpen] = React.useState(false);

  const toggleDropdown = () => {
    setIsOpen(!isOpen);
  };

  return (
    <div className="dropdown">
      <button onClick={toggleDropdown} className="dropdown-btn">
        {selectedOption} ▼
      </button>
      {isOpen && (
        <ul className="dropdown-menu">
          {options.map(option => (
            <li key={option}>
              <button 
                onClick={() => {
                  onSelect(option);
                  setIsOpen(false);
                }} 
                className="dropdown-item"
              >
                {option}
              </button>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default DropdownButton;

import React, { useState } from 'react';
import { modelProviders } from '../data/modelProviders';

const SidebarComponent = () => {
  const [selectedOption, setSelectedOption] = useState<string>('');
  const [selectedSubOption, setSelectedSubOption] = useState<string>('');
  const [apiKey, setApiKey] = useState<string>('');

  const handleOptionChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
    const selectedValue = event.target.value;
    setSelectedOption(selectedValue);
    setSelectedSubOption('');
  };

  const handleSubOptionChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
    const selectedValue = event.target.value;
    setSelectedSubOption(selectedValue);
  };

  const handleApiKeyChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const apiKeyValue = event.target.value;
    setApiKey(apiKeyValue);
  };

  const handleFormSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const formData = {
      selectedOption,
      selectedSubOption,
      apiKey,
    };
    try {
      const response = await fetch('http://localhost:4000/submit-data', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });
      if (!response.ok) {
        throw new Error('Network response was not ok.');
      }
      const responseData = await response.json();
      console.log('Response from Backend:', responseData);
    } catch (error) {
      console.error('Error:', error);
    }
  };

  const selectedOptionData = modelProviders.find((item) => item.value === selectedOption);
  const subOptions = selectedOptionData ? selectedOptionData.subOptions : [];

  return (
    <div className="sidebar">
      <h1>Select Model</h1>
      <form onSubmit={handleFormSubmit}>
        <select className="dropdown-select" value={selectedOption} onChange={handleOptionChange}>
          <option value="">Model Provider</option>
          {modelProviders.map((item, index) => (
            <option key={index} value={item.value}>
              {item.value}
            </option>
          ))}
        </select>
        {selectedOption && (
          <div>
            <select className="dropdown-select" value={selectedSubOption} onChange={handleSubOptionChange}>
              <option value="">Model</option>
              {subOptions.map((subOption, index) => (
                <option key={index} value={subOption.value}>
                  {subOption.value}
                </option>
              ))}
            </select>
          </div>
        )}
        {selectedOption && selectedSubOption && (
          <div>
            <input
              type="text"
              placeholder="Enter API Key"
              value={apiKey}
              onChange={handleApiKeyChange}
            />
          </div>)}
        {selectedOption && selectedSubOption && apiKey && (
          <button type="submit">Submit</button>
        )}
      </form>
    </div>

  );
};

export default SidebarComponent;

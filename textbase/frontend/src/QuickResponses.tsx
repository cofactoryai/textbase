// QuickResponses.tsx

import React, { useState } from "react";

type QuickResponsesProps = {
  onSelectResponse: (response: string) => void;
  quickResponses: string[];
};

const QuickResponses: React.FC<QuickResponsesProps> = ({
  onSelectResponse,
  quickResponses,
}) => {
  const [selectedResponse, setSelectedResponse] = useState<string | null>(null);

  const handleResponseClick = (response: string) => {
    setSelectedResponse(response);
    onSelectResponse(response);
  };

  return (
    <div className="quick-responses">
      <p className="text-gray-400 mb-1">Quick Response Library:</p>
      <div className="grid grid-cols-2 gap-1">
        {quickResponses.map((response, index) => (
          <button
            key={index}
            onClick={() => handleResponseClick(response)}
            className={`py-1 px-2 text-sm text-gray-800 rounded-lg transition ${
              selectedResponse === response
                ? "bg-indigo-100 hover:bg-indigo-200"
                : "bg-gray-100 hover:bg-gray-200"
            }`}
            aria-selected={selectedResponse === response}
          >
            {response}
          </button>
        ))}
      </div>
    </div>
  );
};

export default QuickResponses;

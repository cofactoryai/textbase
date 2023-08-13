
import React from "react";
import "./App.css";
import Bot from "./components/bot";


const App: React.FC = () => {

  // TODO: Use a context provider for complex implementations
  const [state, setState] = React.useState<object>({});

  return (
    <>
      <Bot type="FULL" state={state} setState={setState}/>
    </>
  );
}

export default App;

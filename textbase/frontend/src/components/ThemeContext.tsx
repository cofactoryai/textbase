import React, { createContext, useContext, useState } from 'react';

interface Theme {
  backgroundColor: string;
  foregroundColor: string;
  fontFamily: string;
  avatar: string;
  backgroundImage?: string;
  gradientStart?: string;
  gradientEnd?: string;
}

const defaultTheme: Theme = {
  backgroundColor: '#ffffff',
  foregroundColor: 'grey',
  fontFamily: 'Arial, sans-serif',
  avatar: '',
  backgroundImage: '',
  gradientStart: '#ffffff', 
  gradientEnd: 'grey',
};

const ThemeContext = createContext<{
  theme: Theme;
  setTheme: React.Dispatch<React.SetStateAction<Theme>>;
}>({
  theme: defaultTheme,
  setTheme: () => {},
});

export const ThemeProvider: React.FC = ({ children }) => {
  const [theme, setTheme] = useState<Theme>(defaultTheme);

  return (
    <ThemeContext.Provider value={{ theme, setTheme }}>
      {children}
    </ThemeContext.Provider>
  );
};

export const useTheme = () => {
  return useContext(ThemeContext);
};

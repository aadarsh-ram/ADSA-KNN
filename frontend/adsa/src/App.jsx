import React, { useState } from 'react';
import { Button, TextInput, Header} from '@mantine/core';


function App() {
  const [inputs, setInputs] = useState({
    pregnancies: '',
    glucose: '',
    bloodPressure: '',
    skinThickness: '',
    insulin: '',
    bmi: '',
    diabetesPedigreeFunction: '',
    age: '',
    outcome: ''
  });

  const handleInputChange = (event) => {
    const { name, value } = event.target;
    setInputs((prevInputs) => ({ ...prevInputs, [name]: value }));
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
      
    const serverUrl = 'http://127.0.0.1:8000';
      
    const intInputs = {
      a: parseInt(inputs.pregnancies, 10),
      b: parseInt(inputs.glucose, 10),
      c: parseInt(inputs.bloodPressure, 10),
      d: parseInt(inputs.skinThickness, 10),
      e: parseInt(inputs.insulin, 10),
      f: parseFloat(inputs.bmi),
      g: parseFloat(inputs.diabetesPedigreeFunction),
      h: parseInt(inputs.age, 10),
    };
      
    try {
      const response = await fetch(`${serverUrl}/predict`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(intInputs),
      });
    
      if (!response.ok) {
        throw new Error('There was an error with the request.');
      }
    
      const data = await response.json();
      console.log("so the prediction is ",data.prediction);
      const element = document.getElementById('output'); 
      const prediction = data.prediction === 1.0 ? 'positive' : 'negative';
      element.innerText = `The prediction is ${prediction} for diabetes.`;

    
    } catch (error) {
      console.error(error);
    }
  };
  


return (
  <div>
    <Header order={1}>Diabetes Mellitus Predictor</Header>
    <h2>Enter inputs:</h2>
    <form onSubmit={handleSubmit}>
      <div style={{ marginBottom: '5px' }}>
        <TextInput
          label="Pregnancies"
          description="Number of times pregnant"
          value={inputs.pregnancies}
          name="pregnancies"
          placeholder='Enter number of pregnancies'
          onChange={handleInputChange}
          required
        />
      </div>
      <div style={{ marginBottom: '5px' }}>
        <TextInput
          label="Glucose"
          description="Plasma glucose concentration a 2 hours in an oral glucose tolerance test"
          value={inputs.glucose}
          placeholder='Enter glucose'
          name="glucose"
          onChange={handleInputChange}
          required
        />
      </div>
      <div style={{ marginBottom: '5px' }}>
        <TextInput
          label="Blood Pressure"
          description="Diastolic blood pressure (mm Hg)"
          value={inputs.bloodPressure}
          placeholder='Enter blood pressure'
          name="bloodPressure"
          onChange={handleInputChange}
          required
        />
      </div>
      <div style={{ marginBottom: '5px' }}>
        <TextInput
          label="Skin Thickness"
          description="Triceps skin fold thickness (mm)"
          value={inputs.skinThickness}
          placeholder='Enter skin thickness'
          name="skinThickness"
          onChange={handleInputChange}
          required
        />
      </div>
      <div style={{ marginBottom: '5px' }}>
        <TextInput
          label="Insulin"
          description="2-Hour serum insulin (mu U/ml)"
          value={inputs.insulin}
          placeholder='Enter insulin'
          name="insulin"
          onChange={handleInputChange}
          required
        />
      </div>
      <div style={{ marginBottom: '5px' }}>
        <TextInput
          label="BMI"
          value={inputs.bmi}
          placeholder='Enter BMI'
          description="Body mass index (weight in kg/(height in m)^2)"
          name="bmi"
          onChange={handleInputChange}
          required
        />
      </div>
      <div style={{ marginBottom: '5px' }}>
        <TextInput
          label="Diabetes Pedigree Function"
          value={inputs.diabetesPedigreeFunction}
          name="diabetesPedigreeFunction"
          placeholder='Enter diabetes pedigree function'
          onChange={handleInputChange}
          required
        />
      </div>
      <div style={{ marginBottom: '5px' }}>
        <TextInput
          label="Age"
          value={inputs.age}
          name="age"
          placeholder='Enter age in years'
          onChange={handleInputChange}
          required
        />
      </div>
      <Button type="submit">Submit</Button>
    </form>
    <div id="output"></div>
  </div>
);
}
export default App;

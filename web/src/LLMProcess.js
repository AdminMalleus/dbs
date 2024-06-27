import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import io from 'socket.io-client';
import ReactMarkdown from 'react-markdown';
import './LLMProcess.css';
import Modal from './Modal';

const LLMProcess = () => {
    const [text, setText] = useState('');
    const [models, setModels] = useState([]);
    const [categories, setCategories] = useState([]);
    const [promptModels, setPromptModels] = useState({});
    const [promptTexts, setPromptTexts] = useState({});
    const [responses, setResponses] = useState({});
    const [activeTab, setActiveTab] = useState('');
    const [activeModal, setActiveModal] = useState(null);
    const [selectedCategories, setSelectedCategories] = useState({});
    const [manualScroll, setManualScroll] = useState({});
    const responseContainerRefs = useRef({});
    const [showScrollButton, setShowScrollButton] = useState({});

    useEffect(() => {
      const fetchData = async () => {
        try {
          const [modelsResponse, categoriesResponse, promptsResponse] = await Promise.all([
            axios.get('https://dbsbackend.azurewebsites.net/get_models'),
            axios.get('https://dbsbackend.azurewebsites.net/get_categories'),
            axios.get('https://dbsbackend.azurewebsites.net/get_prompts')
          ]);
          
          const fetchedModels = modelsResponse.data.models;
          const fetchedCategories = categoriesResponse.data.categories;
          const prompts = promptsResponse.data.prompts;
    
          setModels(fetchedModels);
          setCategories(fetchedCategories);
    
          if (fetchedModels.length > 0 && fetchedCategories.length > 0) {
            const defaultModel = fetchedModels[0];
            const initialPromptModels = {};
            const initialPromptTexts = {};
            const initialResponses = {};
            const initialSelectedCategories = {};
            const initialManualScroll = {};
            const initialResponseContainerRefs = {};
    
            fetchedCategories.forEach(category => {
              initialPromptModels[category] = defaultModel;
              initialPromptTexts[category] = prompts[category] || '';
              initialResponses[category] = '';
              initialSelectedCategories[category] = true;
              initialManualScroll[category] = false;
              initialResponseContainerRefs[category] = React.createRef();
            });
    
            setPromptModels(initialPromptModels);
            setPromptTexts(initialPromptTexts);
            setResponses(initialResponses);
            setSelectedCategories(initialSelectedCategories);
            setManualScroll(initialManualScroll);
            responseContainerRefs.current = initialResponseContainerRefs;
    
            // Set the active tab to the first category (since all are initially selected)
            setActiveTab(fetchedCategories[0]);
          }
        } catch (error) {
          console.error('Failed to fetch data:', error);
        }
      };
    
      fetchData();
    }, []);

    useEffect(() => {
      Object.entries(responseContainerRefs.current).forEach(([category, ref]) => {
        if (ref && !manualScroll[category]) {
          ref.scrollTop = ref.scrollHeight;
        }
      });
    }, [responses, manualScroll]);

  const handleScroll = (category) => {
    const container = responseContainerRefs.current[category];
    if (container) {
      const { scrollTop, scrollHeight, clientHeight } = container;
      const isScrolledToBottom = Math.abs(scrollHeight - scrollTop - clientHeight) < 1;
      
      setManualScroll(prev => ({
        ...prev,
        [category]: !isScrolledToBottom
      }));
  
      setShowScrollButton(prev => ({
        ...prev,
        [category]: !isScrolledToBottom && scrollHeight > clientHeight
      }));
    }
  };
  const scrollToBottom = (category) => {
    const container = responseContainerRefs.current[category];
    if (container) {
      container.scrollTop = container.scrollHeight;
      setManualScroll(prev => ({
        ...prev,
        [category]: false
      }));
      setShowScrollButton(prev => ({
        ...prev,
        [category]: false
      }));
    }
  };
  useEffect(() => {
    if (activeTab) {
      const container = responseContainerRefs.current[activeTab];
      if (container) {
        container.scrollTop = container.scrollHeight;
      }
    }
  }, [activeTab]);

  const resetScroll = (category) => {
    setManualScroll(prev => ({
      ...prev,
      [category]: false
    }));
    setShowScrollButton(prev => ({
      ...prev,
      [category]: false
    }));
    const container = responseContainerRefs.current[category];
    if (container) {
      container.scrollTop = container.scrollHeight;
    }
  };

  useEffect(() => {
    if (categories.length === 0) return;
  
    const newSockets = {};
    categories.forEach((category, index) => {
      const socket = io(`https://dbsbackend.azurewebsites.net/prompt${index + 1}`, {
        transports: ['websocket'],
        upgrade: false
      });      newSockets[category] = socket;
  
      socket.on('response', (data) => {
        if (data.response === '[DONE]') {
          console.log(`Processing done for ${category}.`);
          resetScroll(category);
        } else {
          setResponses(prevResponses => ({
            ...prevResponses,
            [category]: (prevResponses[category] || '') + data.response
          }));
        }
      });
  
      socket.on('connect', () => console.log(`Connected to socket for ${category}`));
      socket.on('disconnect', () => console.log(`Disconnected from socket for ${category}`));
      socket.on('connect_error', (err) => console.error(`Socket connection error for ${category}:`, err));
    });
  
    return () => {
      Object.values(newSockets).forEach(socket => socket.disconnect());
    };
  }, [categories]);

  useEffect(() => {
    Object.entries(responseContainerRefs.current).forEach(([category, ref]) => {
      if (ref) {
        ref.scrollTop = ref.scrollHeight;
      }
    });
  }, [responses]);

  const handleProcess = async () => {
    const initialResponses = {};
    categories.forEach(category => {
      if (selectedCategories[category]) {
        initialResponses[category] = '';
      }
    });
    setResponses(initialResponses);
  
    try {
      const selectedPromptModels = {};
      const selectedPromptTexts = {};
      
      Object.keys(selectedCategories).forEach(category => {
        if (selectedCategories[category]) {
          selectedPromptModels[category] = promptModels[category];
          selectedPromptTexts[category] = promptTexts[category];
        }
      });
  
      await axios.post('https://dbsbackend.azurewebsites.net/process', { 
        text, 
        promptModels: selectedPromptModels, 
        promptTexts: selectedPromptTexts 
      });
    } catch (error) {
      console.error('Error processing the request:', error);
      setResponses(prevResponses => ({
        ...prevResponses,
        [activeTab]: 'An error occurred while processing your request.'
      }));
    }
  };
  const handleCategoryToggle = (category) => {
    setSelectedCategories(prevState => {
      const newState = {
        ...prevState,
        [category]: !prevState[category]
      };
      
      // If we're unchecking the active tab, switch to the first available tab
      if (category === activeTab && !newState[category]) {
        const nextActiveTab = categories.find(cat => newState[cat]);
        setActiveTab(nextActiveTab || '');
      }
      
      return newState;
    });
  };
  const handlePromptModelChange = (category, value) => {
    setPromptModels(prevState => ({
      ...prevState,
      [category]: value
    }));
  };

  const handlePromptTextChange = (category, value) => {
    setPromptTexts(prevState => ({
      ...prevState,
      [category]: value
    }));
  };

  const openModal = (category) => {
    setActiveModal(category);
  };

  const closeModal = () => {
    setActiveModal(null);
  };

  return (
    <div className="container">
      <div className="input-container">
        <h3 className="header">Input:</h3>
        <textarea
          value={text}
          onChange={(e) => setText(e.target.value)}
          placeholder="Enter your text here..."
          className="textarea"
        />
        <div className="process-controls">
          <div className="category-checkboxes">
            {categories.map((category) => (
              <label key={category} className="checkbox-label">
                <input
                  type="checkbox"
                  checked={selectedCategories[category]}
                  onChange={() => handleCategoryToggle(category)}
                />
                {category}
              </label>
            ))}
          </div>
          <button onClick={handleProcess} className="process-button">
            Process
          </button>
        </div>
      </div>
  
      <div className="response-container">
      <div className="tabs">
        {categories.map((category) => (
          selectedCategories[category] && (
            <div key={category} className="tab-container">
              <div className="model-dropdown">
                <select
                  value={promptModels[category]}
                  onChange={(e) => handlePromptModelChange(category, e.target.value)}
                >
                  {models.map(model => (
                    <option key={model} value={model}>{model}</option>
                  ))}
                </select>
              </div>
              <button
                className={`tab ${activeTab === category ? 'active' : ''}`}
                onClick={() => setActiveTab(category)}
              >
                {category}
              </button>
              <button onClick={() => openModal(category)} className="settings-button">
                ⚙️
              </button>
            </div>
          )
        ))}
      </div>
      <div className="responses">
      {categories.map((category) => (
        selectedCategories[category] && (
          <div key={category} className="response-wrapper">
            <div
              className={`response ${activeTab === category ? 'active' : ''}`}
              ref={el => responseContainerRefs.current[category] = el}
              onScroll={() => handleScroll(category)}
            >
              <ReactMarkdown>{responses[category] || ''}</ReactMarkdown>
            </div>
              {showScrollButton[category] && (
                <button 
                  className="scroll-to-bottom-button"
                  onClick={() => scrollToBottom(category)}
                >
                  ▼
                </button>
              )}
            </div>
          )
        ))}
      </div>
      </div>
  
      {categories.map((category) => (
        <Modal key={category} isOpen={activeModal === category} onClose={closeModal}>
        <h2>{category} Settings</h2>
        <h3>Prompt Text:</h3>
        <textarea
          value={promptTexts[category]}
          onChange={(e) => handlePromptTextChange(category, e.target.value)}
          className="modal-textarea"
          placeholder={`Enter ${category} text here...`}
        />
        <button onClick={closeModal} className="modal-save-button">Save</button>
      </Modal>
      ))}
    </div>
  );
};

export default LLMProcess;
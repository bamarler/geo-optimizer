import { useState } from 'react';
import UrlInput from './components/UrlInput';
import ContentDisplay from './components/ContentDisplay';
import Header from './components/Header';
import LoadingSpinner from './components/LoadingSpinner';
import PersonaGenerator from './components/PersonaGenerator';
import PersonaCard from './components/PersonaCard';
import BrandDescription from './components/BrandDescription';
import PromptGenerator from './components/PromptGenerator';
import PromptList from './components/PromptList';
import TestingProgress from './components/TestingProgress';
import TestResults from './components/TestResults';

function App() {
  const [step, setStep] = useState('input'); // 'input', 'scraping', 'description', 'generate', 'generating', 'personas', 'prompts', 'promptsReview', 'testing', 'results'
  const [loading, setLoading] = useState(false);
  const [scrapedData, setScrapedData] = useState(null);
  const [brandDescription, setBrandDescription] = useState('');
  const [personas, setPersonas] = useState([]);
  const [personaSetId, setPersonaSetId] = useState('');
  const [prompts, setPrompts] = useState([]);
  const [promptsId, setPromptsId] = useState('');
  const [testResults, setTestResults] = useState(null);
  const [error, setError] = useState(null);

  const handleScrape = async (url) => {
    setLoading(true);
    setError(null);
    setScrapedData(null);
    setStep('scraping');

    try {
      const response = await fetch('/api/scrape', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ url }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || 'Failed to scrape website');
      }

      setScrapedData(data);
      setBrandDescription(data.brand_summary || '');
      setStep('description');
    } catch (err) {
      setError(err.message);
      setStep('input');
    } finally {
      setLoading(false);
    }
  };

  const handleBrandDescriptionApprove = (approvedDescription) => {
    setBrandDescription(approvedDescription);
    setStep('generate');
  };

  const handlePersonasGenerated = (generatedPersonas) => {
    setPersonas(generatedPersonas);
    setStep('personas');
  };

  const handleUpdatePersona = (index, updatedPersona) => {
    const newPersonas = [...personas];
    newPersonas[index] = updatedPersona;
    setPersonas(newPersonas);
  };

  const handleDeletePersona = (index) => {
    setPersonas(personas.filter((_, i) => i !== index));
  };

  const handleApprovePersonas = async () => {
    // Save personas to database
    try {
      const response = await fetch('/api/personas/save', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          personas: personas,
          website_url: scrapedData.url,
          website_title: scrapedData.title,
          brand_description: brandDescription,
        }),
      });

      const data = await response.json();

      if (response.ok) {
        setPersonaSetId(data.id);
        setStep('prompts');
      } else {
        alert(`⚠️ Failed to save personas:\n${data.message || data.error}`);
      }
    } catch (err) {
      alert(`⚠️ Failed to save personas:\n${err.message}`);
    }
  };

  const handlePromptsGenerated = (generatedPrompts) => {
    setPrompts(generatedPrompts);
    setStep('promptsReview');
  };

  const handleUpdatePrompt = (index, updatedPrompt) => {
    const newPrompts = [...prompts];
    newPrompts[index] = updatedPrompt;
    setPrompts(newPrompts);
  };

  const handleDeletePrompt = (index) => {
    setPrompts(prompts.filter((_, i) => i !== index));
  };

  const handleApprovePrompts = async () => {
    // Save prompts to database
    try {
      const saveResponse = await fetch('/api/prompts/save', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          prompts: prompts,
          persona_set_id: personaSetId,
          website_url: scrapedData.url,
          website_title: scrapedData.title,
        }),
      });

      const saveData = await saveResponse.json();

      if (saveResponse.ok) {
        const savedPromptsId = saveData.id;
        setPromptsId(savedPromptsId);
        
        // Ask user if they want to start GEO testing
        const startTesting = window.confirm(
          `✅ Success! ${personas.length} personas and ${prompts.length} prompts saved!\n\n` +
          `Would you like to start GEO testing now?\n\n` +
          `This will:\n` +
          `• Open ChatGPT in a browser\n` +
          `• Test each persona with each prompt\n` +
          `• Record all responses to MongoDB\n` +
          `• Run ${personas.length} × ${prompts.length} = ${personas.length * prompts.length} tests\n\n` +
          `Click OK to start testing, or Cancel to skip for now.`
        );

        if (startTesting) {
          // Trigger GEO testing
          const testResponse = await fetch('/api/run-geo-test', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({
              persona_set_id: personaSetId,
              prompts_id: savedPromptsId,
            }),
          });

          const testData = await testResponse.json();

          if (testResponse.ok) {
            // Navigate to testing progress screen
            setStep('testing');
          } else {
            alert(`⚠️ Failed to start GEO testing:\n${testData.message || testData.error}`);
          }
        } else {
          alert(`✅ Data saved! You can run GEO testing later from MongoDB.`);
        }
      } else {
        alert(`⚠️ Failed to save prompts:\n${saveData.message || saveData.error}`);
      }
    } catch (err) {
      alert(`⚠️ Failed to save prompts:\n${err.message}`);
    }
  };

  const handleTestingComplete = (resultsData) => {
    setTestResults(resultsData);
    setStep('results');
  };

  const handleStartOver = () => {
    setStep('input');
    setScrapedData(null);
    setBrandDescription('');
    setPersonas([]);
    setPersonaSetId('');
    setPrompts([]);
    setPromptsId('');
    setTestResults(null);
    setError(null);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100">
      <Header />
      
      <main className="container mx-auto px-4 py-12 max-w-6xl">
        <div className="space-y-8">
          {/* Hero Section */}
          <div className="text-center space-y-4">
            <h1 className="text-5xl font-bold text-gray-900 tracking-tight">
              GEO Optimizer
            </h1>
            <p className="text-xl text-gray-600 max-w-2xl mx-auto">
              Analyze websites, generate personas, and optimize for generative AI engines.
            </p>
          </div>

          {/* Progress Steps */}
          {step !== 'input' && (
            <div className="flex items-center justify-center space-x-2 max-w-4xl mx-auto overflow-x-auto">
              <StepIndicator number={1} label="Analyze" active={step === 'scraping'} completed={['description', 'generate', 'generating', 'personas', 'prompts', 'promptsReview'].includes(step)} />
              <div className={`h-1 w-8 ${['description', 'generate', 'generating', 'personas', 'prompts', 'promptsReview'].includes(step) ? 'bg-primary-500' : 'bg-gray-300'}`}></div>
              <StepIndicator number={2} label="Description" active={step === 'description'} completed={['generate', 'generating', 'personas', 'prompts', 'promptsReview'].includes(step)} />
              <div className={`h-1 w-8 ${['generate', 'generating', 'personas', 'prompts', 'promptsReview'].includes(step) ? 'bg-primary-500' : 'bg-gray-300'}`}></div>
              <StepIndicator number={3} label="Personas" active={step === 'generating'} completed={['personas', 'prompts', 'promptsReview'].includes(step)} />
              <div className={`h-1 w-8 ${['personas', 'prompts', 'promptsReview'].includes(step) ? 'bg-primary-500' : 'bg-gray-300'}`}></div>
              <StepIndicator number={4} label="Review" active={step === 'personas'} completed={['prompts', 'promptsReview'].includes(step)} />
              <div className={`h-1 w-8 ${['prompts', 'promptsReview'].includes(step) ? 'bg-primary-500' : 'bg-gray-300'}`}></div>
              <StepIndicator number={5} label="Prompts" active={step === 'prompts'} completed={step === 'promptsReview'} />
              <div className={`h-1 w-8 ${step === 'promptsReview' ? 'bg-primary-500' : 'bg-gray-300'}`}></div>
              <StepIndicator number={6} label="Approve" active={step === 'promptsReview'} completed={false} />
            </div>
          )}

          {/* Step 1: URL Input */}
          {step === 'input' && (
            <div className="card max-w-3xl mx-auto">
              <UrlInput onScrape={handleScrape} loading={loading} />
            </div>
          )}

          {/* Loading State */}
          {loading && (
            <div className="flex justify-center py-12">
              <LoadingSpinner />
            </div>
          )}

          {/* Error Display */}
          {error && (
            <div className="card max-w-3xl mx-auto bg-red-50 border-red-200">
              <div className="flex items-start space-x-3">
                <svg className="w-6 h-6 text-red-500 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                <div>
                  <h3 className="text-lg font-semibold text-red-800">Error</h3>
                  <p className="text-red-600 mt-1">{error}</p>
                  <button onClick={handleStartOver} className="text-sm text-red-700 underline mt-2">
                    Start Over
                  </button>
                </div>
              </div>
            </div>
          )}

          {/* Step 2: Review Brand Description */}
          {step === 'description' && scrapedData && (
            <>
              <div className="card max-w-4xl mx-auto bg-green-50 border-green-200 mb-6">
                <div className="flex items-center space-x-3">
                  <svg className="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  <div className="flex-1">
                    <h3 className="text-lg font-semibold text-green-800">Website Analyzed Successfully!</h3>
                    <p className="text-green-700 mt-1">
                      <strong>{scrapedData.title}</strong> • Analysis complete
                    </p>
                  </div>
                </div>
              </div>
              <BrandDescription 
                initialDescription={brandDescription}
                websiteTitle={scrapedData.title}
                onApprove={handleBrandDescriptionApprove}
              />
            </>
          )}

          {/* Step 3: Generate Personas */}
          {step === 'generate' && scrapedData && (
            <PersonaGenerator 
              scrapedData={{...scrapedData, brand_summary: brandDescription}} 
              onPersonasGenerated={handlePersonasGenerated} 
            />
          )}

          {/* Step 4: Review Personas */}
          {step === 'personas' && personas.length > 0 && (
            <>
              <div className="text-center space-y-4">
                <h2 className="text-3xl font-bold text-gray-900">Review Your Personas</h2>
                <p className="text-gray-600">Edit any details or approve to continue</p>
              </div>

              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 max-w-6xl mx-auto">
                {personas.map((persona, index) => (
                  <PersonaCard
                    key={index}
                    persona={persona}
                    index={index}
                    onUpdate={handleUpdatePersona}
                    onDelete={handleDeletePersona}
                  />
                ))}
              </div>

              <div className="flex justify-center space-x-4">
                <button
                  onClick={handleStartOver}
                  className="px-6 py-3 bg-gray-200 hover:bg-gray-300 text-gray-800 font-medium rounded-lg transition-colors"
                >
                  Start Over
                </button>
                <button
                  onClick={handleApprovePersonas}
                  className="btn-primary"
                >
                  Save & Generate Prompts →
                </button>
              </div>
            </>
          )}

          {/* Step 5: Generate Prompts */}
          {step === 'prompts' && (
            <PromptGenerator
              brandDescription={brandDescription}
              websiteTitle={scrapedData.title}
              websiteAnalysis={scrapedData.content}
              onPromptsGenerated={handlePromptsGenerated}
            />
          )}

          {/* Step 6: Review Prompts */}
          {step === 'promptsReview' && prompts.length > 0 && (
            <PromptList
              prompts={prompts}
              onApprove={handleApprovePrompts}
              onUpdate={handleUpdatePrompt}
              onDelete={handleDeletePrompt}
            />
          )}
        </div>
      </main>

      {/* Testing Progress Screen (Fullscreen) */}
      {step === 'testing' && (
        <TestingProgress
          personaSetId={personaSetId}
          promptsId={promptsId}
          totalTests={personas.length * prompts.length}
          onComplete={handleTestingComplete}
        />
      )}

      {/* Results Screen */}
      {step === 'results' && testResults && (
        <TestResults
          results={testResults.results || []}
          stats={testResults.stats || {}}
          analysis={testResults.analysis || {}}
          websiteTitle={testResults.website_title || scrapedData?.title || 'Unknown Website'}
          onStartOver={handleStartOver}
        />
      )}

      {/* Footer */}
      <footer className="container mx-auto px-4 py-8 text-center text-gray-500 text-sm">
        <p>Powered by Perplexity AI & OpenAI • Built for GEO Optimization</p>
      </footer>
    </div>
  );
}

function StepIndicator({ number, label, active, completed }) {
  return (
    <div className="flex flex-col items-center">
      <div className={`w-10 h-10 rounded-full flex items-center justify-center font-semibold transition-all ${
        completed ? 'bg-primary-600 text-white' :
        active ? 'bg-primary-600 text-white animate-pulse' :
        'bg-gray-300 text-gray-600'
      }`}>
        {completed ? '✓' : number}
      </div>
      <span className={`text-xs mt-1 ${active || completed ? 'text-gray-900 font-medium' : 'text-gray-500'}`}>
        {label}
      </span>
    </div>
  );
}

export default App;

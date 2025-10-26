import { useState, useEffect } from 'react';

export default function TestingProgress({ personaSetId, promptsId, totalTests, onComplete }) {
  const [status, setStatus] = useState('starting');
  const [message, setMessage] = useState('Initializing GEO testing...');

  useEffect(() => {
    // Simulate progress updates
    const stages = [
      { delay: 2000, status: 'running', message: '🚀 Browser launched. Opening ChatGPT...' },
      { delay: 5000, status: 'running', message: '🔐 Loading authenticated session...' },
      { delay: 8000, status: 'running', message: '🧹 Clearing ChatGPT memory...' },
      { delay: 11000, status: 'running', message: '👤 Setting first persona...' },
      { delay: 14000, status: 'running', message: '📤 Sending test prompts...' },
      { delay: 20000, status: 'running', message: `⏳ Running ${totalTests} tests. This may take several minutes...` },
      { delay: 25000, status: 'running', message: '📊 Recording responses to MongoDB...' },
      { delay: 40000, status: 'checking', message: '🔍 Checking for results...' },
    ];

    stages.forEach(({ delay, status: newStatus, message: newMessage }) => {
      setTimeout(() => {
        setStatus(newStatus);
        setMessage(newMessage);
      }, delay);
    });

    // Check for results periodically
    const checkResults = setInterval(async () => {
      try {
        const response = await fetch(`http://localhost:5001/api/test-results/${personaSetId}`);
        
        if (response.ok) {
          const data = await response.json();
          
          // FIXED: Wait for ALL tests to complete, not just first result
          // Only show analytics when we have all expected results
          if (data.success && data.results && data.results.length >= totalTests) {
            clearInterval(checkResults);
            setStatus('complete');
            setMessage(`✅ Testing complete! All ${data.results.length} tests finished.`);
            console.log('All test results retrieved:', data);
            setTimeout(() => onComplete(data), 2000);
          } else if (data.results && data.results.length > 0) {
            // Show progress: some results received, but not all yet
            console.log(`Progress: ${data.results.length}/${totalTests} tests complete...`);
            setMessage(`⏳ Testing in progress: ${data.results.length}/${totalTests} tests complete...`);
          }
        } else if (response.status === 404) {
          // Results not ready yet, keep checking
          console.log('Results not ready yet, continuing to check...');
        }
      } catch (err) {
        console.error('Error checking results:', err);
      }
    }, 8000); // Check every 8 seconds

    return () => clearInterval(checkResults);
  }, [personaSetId, totalTests, onComplete]);

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-gray-50 to-gray-100 px-4">
      <div className="card max-w-2xl w-full">
        <div className="text-center space-y-8">
          {/* Animated Icon */}
          <div className="relative inline-block">
            <div className="w-32 h-32 bg-gradient-to-br from-primary-500 to-primary-700 rounded-full flex items-center justify-center animate-pulse">
              {status === 'complete' ? (
                <svg className="w-16 h-16 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={3} d="M5 13l4 4L19 7" />
                </svg>
              ) : (
                <svg className="w-16 h-16 text-white animate-spin" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
              )}
            </div>
          </div>

          {/* Title */}
          <div>
            <h2 className="text-3xl font-bold text-gray-900 mb-2">
              {status === 'complete' ? 'Testing Complete!' : 'GEO Testing In Progress'}
            </h2>
            <p className="text-lg text-gray-600">{message}</p>
          </div>

          {/* Progress Info */}
          <div className="bg-gray-50 rounded-lg p-6 space-y-4">
            <div className="flex items-center justify-between text-sm">
              <span className="text-gray-600">Total Tests:</span>
              <span className="font-semibold text-gray-900">{totalTests}</span>
            </div>
            <div className="flex items-center justify-between text-sm">
              <span className="text-gray-600">Status:</span>
              <span className={`font-semibold ${
                status === 'complete' ? 'text-green-600' : 
                status === 'checking' ? 'text-yellow-600' : 
                'text-primary-600'
              }`}>
                {status === 'complete' ? 'Complete ✓' : 
                 status === 'checking' ? 'Checking Results...' : 
                 'Running...'}
              </span>
            </div>
          </div>

          {/* Info Box */}
          <div className="bg-blue-50 rounded-lg p-4 text-left">
            <div className="flex items-start space-x-3">
              <svg className="w-5 h-5 text-blue-600 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <div className="text-sm text-blue-800">
                <p className="font-medium mb-1">What's happening?</p>
                <ul className="space-y-1 text-blue-700">
                  <li>• Browser is testing each persona with each prompt</li>
                  <li>• ChatGPT responses are being recorded</li>
                  <li>• Results are being saved to MongoDB</li>
                  <li>• This process runs automatically in the background</li>
                </ul>
              </div>
            </div>
          </div>

          {status !== 'complete' && (
            <p className="text-sm text-gray-500">
              Please wait... Do not close this window.
            </p>
          )}
        </div>
      </div>
    </div>
  );
}


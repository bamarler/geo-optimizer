import { useState } from 'react';

export default function TestResults({ results, stats, analysis, websiteTitle, onStartOver }) {
  const [selectedResult, setSelectedResult] = useState(null);
  const [filter, setFilter] = useState('all'); // all, with_citations, brand_mentioned
  const [showAnalysis, setShowAnalysis] = useState(true);

  const filteredResults = results.filter(r => {
    if (filter === 'with_citations') return r.has_citations;
    if (filter === 'brand_mentioned') return r.brand_mentioned;
    return true;
  });

  const brandMentionPercent = (stats.brand_mention_rate * 100).toFixed(1);
  const citationPercent = (stats.citation_rate * 100).toFixed(1);
  
  // Get AI analysis score and color
  const getScoreColor = (score) => {
    if (!score) return 'text-gray-500';
    if (score >= 70) return 'text-green-600';
    if (score >= 40) return 'text-yellow-600';
    return 'text-red-600';
  };

  return (
    <div className="max-w-7xl mx-auto px-4 py-8">
      {/* Header */}
      <div className="text-center mb-8">
        <h1 className="text-4xl font-bold text-gray-900 mb-2">GEO Test Results</h1>
        <p className="text-gray-600">Analysis complete for <strong className="text-primary-600">{websiteTitle}</strong></p>
      </div>

      {/* Stats Overview */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
        <div className="card text-center">
          <div className="text-3xl font-bold text-primary-600 mb-2">{stats.total_tests}</div>
          <div className="text-sm text-gray-600">Total Tests</div>
        </div>
        <div className="card text-center">
          <div className="text-3xl font-bold text-green-600 mb-2">{brandMentionPercent}%</div>
          <div className="text-sm text-gray-600">Brand Mentions</div>
        </div>
        <div className="card text-center">
          <div className="text-3xl font-bold text-blue-600 mb-2">{citationPercent}%</div>
          <div className="text-sm text-gray-600">With Citations</div>
        </div>
        <div className="card text-center">
          <div className="text-3xl font-bold text-purple-600 mb-2">{stats.with_citations}</div>
          <div className="text-sm text-gray-600">Total Citations</div>
        </div>
      </div>

      {/* Performance Indicator */}
      <div className={`card mb-8 ${
        brandMentionPercent >= 50 ? 'bg-green-50 border-green-200' :
        brandMentionPercent >= 25 ? 'bg-yellow-50 border-yellow-200' :
        'bg-red-50 border-red-200'
      }`}>
        <div className="flex items-center space-x-4">
          <div className={`w-12 h-12 rounded-full flex items-center justify-center ${
            brandMentionPercent >= 50 ? 'bg-green-500' :
            brandMentionPercent >= 25 ? 'bg-yellow-500' :
            'bg-red-500'
          }`}>
            {brandMentionPercent >= 50 ? (
              <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={3} d="M5 13l4 4L19 7" />
              </svg>
            ) : (
              <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={3} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
              </svg>
            )}
          </div>
          <div className="flex-1">
            <h3 className={`text-lg font-semibold ${
              brandMentionPercent >= 50 ? 'text-green-800' :
              brandMentionPercent >= 25 ? 'text-yellow-800' :
              'text-red-800'
            }`}>
              {brandMentionPercent >= 50 ? 'Excellent GEO Performance!' :
               brandMentionPercent >= 25 ? 'Moderate GEO Performance' :
               'Low GEO Visibility'}
            </h3>
            <p className={`text-sm ${
              brandMentionPercent >= 50 ? 'text-green-700' :
              brandMentionPercent >= 25 ? 'text-yellow-700' :
              'text-red-700'
            }`}>
              {brandMentionPercent >= 50 ? 
                'Your brand appears frequently in AI responses. Great job!' :
               brandMentionPercent >= 25 ?
                'Your brand appears in some responses. Consider optimizing your content.' :
                'Your brand rarely appears. Focus on improving content relevance and authority.'}
            </p>
          </div>
        </div>
      </div>

      {/* AI Analysis Section */}
      {analysis && analysis.score !== null && (
        <div className="card mb-8 bg-gradient-to-br from-blue-50 to-purple-50 border-blue-200">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-2xl font-bold text-gray-900 flex items-center">
              <svg className="w-8 h-8 mr-2 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
              </svg>
              AI-Powered GEO Analysis
            </h3>
            <button
              onClick={() => setShowAnalysis(!showAnalysis)}
              className="text-blue-600 hover:text-blue-800 font-medium"
            >
              {showAnalysis ? 'Hide' : 'Show'} Analysis
            </button>
          </div>

          {showAnalysis && (
            <>
              {/* GEO Score */}
              <div className="flex items-center justify-center mb-6">
                <div className="text-center">
                  <div className={`text-6xl font-bold ${getScoreColor(analysis.score)}`}>
                    {analysis.score}
                  </div>
                  <div className="text-gray-600 text-sm mt-1">GEO Performance Score</div>
                </div>
              </div>

              {/* Key Insights */}
              {analysis.insights && analysis.insights.length > 0 && (
                <div className="mb-6">
                  <h4 className="font-semibold text-gray-900 mb-2 flex items-center">
                    <svg className="w-5 h-5 mr-1 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                    Key Insights
                  </h4>
                  <ul className="space-y-2">
                    {analysis.insights.map((insight, idx) => (
                      <li key={idx} className="flex items-start">
                        <span className="text-blue-600 mr-2">•</span>
                        <span className="text-gray-700">{insight}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              )}

              {/* Strengths & Weaknesses Grid */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
                {/* Strengths */}
                {analysis.strengths && analysis.strengths.length > 0 && (
                  <div>
                    <h4 className="font-semibold text-green-700 mb-2 flex items-center">
                      <svg className="w-5 h-5 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                      </svg>
                      Strengths
                    </h4>
                    <ul className="space-y-1">
                      {analysis.strengths.map((strength, idx) => (
                        <li key={idx} className="text-sm text-gray-700 flex items-start">
                          <span className="text-green-600 mr-2">✓</span>
                          {strength}
                        </li>
                      ))}
                    </ul>
                  </div>
                )}

                {/* Weaknesses */}
                {analysis.weaknesses && analysis.weaknesses.length > 0 && (
                  <div>
                    <h4 className="font-semibold text-red-700 mb-2 flex items-center">
                      <svg className="w-5 h-5 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                      </svg>
                      Weaknesses
                    </h4>
                    <ul className="space-y-1">
                      {analysis.weaknesses.map((weakness, idx) => (
                        <li key={idx} className="text-sm text-gray-700 flex items-start">
                          <span className="text-red-600 mr-2">!</span>
                          {weakness}
                        </li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>

              {/* Recommendations */}
              {analysis.recommendations && analysis.recommendations.length > 0 && (
                <div className="bg-blue-100 rounded-lg p-4">
                  <h4 className="font-semibold text-blue-900 mb-2 flex items-center">
                    <svg className="w-5 h-5 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4" />
                    </svg>
                    Actionable Recommendations
                  </h4>
                  <ol className="space-y-2">
                    {analysis.recommendations.map((rec, idx) => (
                      <li key={idx} className="text-sm text-blue-900 flex items-start">
                        <span className="font-bold mr-2">{idx + 1}.</span>
                        <span>{rec}</span>
                      </li>
                    ))}
                  </ol>
                </div>
              )}
            </>
          )}
        </div>
      )}

      {/* Filter Buttons */}
      <div className="flex space-x-2 mb-6">
        <button
          onClick={() => setFilter('all')}
          className={`px-4 py-2 rounded-lg font-medium transition-colors ${
            filter === 'all' ? 'bg-primary-600 text-white' : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
          }`}
        >
          All ({results.length})
        </button>
        <button
          onClick={() => setFilter('brand_mentioned')}
          className={`px-4 py-2 rounded-lg font-medium transition-colors ${
            filter === 'brand_mentioned' ? 'bg-green-600 text-white' : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
          }`}
        >
          Brand Mentioned ({stats.brand_mentioned})
        </button>
        <button
          onClick={() => setFilter('with_citations')}
          className={`px-4 py-2 rounded-lg font-medium transition-colors ${
            filter === 'with_citations' ? 'bg-blue-600 text-white' : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
          }`}
        >
          With Citations ({stats.with_citations})
        </button>
      </div>

      {/* Results List */}
      <div className="space-y-4 mb-8">
        {filteredResults.length === 0 ? (
          <div className="card text-center py-12">
            <p className="text-gray-500">No results match the selected filter.</p>
          </div>
        ) : (
          filteredResults.map((result, idx) => (
            <div
              key={idx}
              className="card hover:shadow-xl transition-shadow cursor-pointer"
              onClick={() => setSelectedResult(selectedResult === idx ? null : idx)}
            >
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <div className="flex items-center space-x-3 mb-2">
                    <span className="text-sm font-medium text-gray-500">
                      Test {result.test_number || idx + 1}
                    </span>
                    {result.has_citations && (
                      <span className="px-2 py-1 bg-blue-100 text-blue-800 text-xs rounded-full">
                        {result.citations?.length || 0} Citations
                      </span>
                    )}
                    {result.brand_mentioned && (
                      <span className="px-2 py-1 bg-green-100 text-green-800 text-xs rounded-full">
                        ✓ Brand Mentioned
                      </span>
                    )}
                  </div>
                  <h4 className="font-semibold text-gray-900 mb-2">
                    {result.prompt_details?.prompt || 'No prompt'}
                  </h4>
                  <p className="text-sm text-gray-600 mb-2">
                    Persona: <strong>{result.persona_details?.name || 'Unknown'}</strong> ({result.persona_details?.location || 'Unknown'})
                  </p>
                  
                  {selectedResult === idx && (
                    <div className="mt-4 pt-4 border-t border-gray-200">
                      <h5 className="font-medium text-gray-900 mb-2">ChatGPT Response:</h5>
                      <div className="bg-gray-50 rounded-lg p-4">
                        <p className="text-gray-800 whitespace-pre-wrap">
                          {result.response_text || 'No response recorded'}
                        </p>
                      </div>
                      
                      {result.citations && result.citations.length > 0 && (
                        <div className="mt-4">
                          <h5 className="font-medium text-gray-900 mb-2">Citations:</h5>
                          <ul className="space-y-2">
                            {result.citations.map((citation, cidx) => (
                              <li key={cidx} className="flex items-start space-x-2 text-sm">
                                <span className="text-primary-600">[{cidx + 1}]</span>
                                <a href={citation.url} target="_blank" rel="noopener noreferrer" className="text-blue-600 hover:underline">
                                  {citation.title || citation.url}
                                </a>
                              </li>
                            ))}
                          </ul>
                        </div>
                      )}
                    </div>
                  )}
                </div>
                
                <svg 
                  className={`w-6 h-6 text-gray-400 transition-transform ${selectedResult === idx ? 'rotate-180' : ''}`}
                  fill="none" 
                  stroke="currentColor" 
                  viewBox="0 0 24 24"
                >
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                </svg>
              </div>
            </div>
          ))
        )}
      </div>

      {/* Actions */}
      <div className="flex justify-center space-x-4">
        <button
          onClick={onStartOver}
          className="px-6 py-3 bg-gray-200 hover:bg-gray-300 text-gray-800 font-medium rounded-lg transition-colors"
        >
          Test Another Website
        </button>
        <button
          onClick={() => window.open('/analytics', '_blank')}
          className="btn-primary"
        >
          View Full Analytics →
        </button>
      </div>
    </div>
  );
}


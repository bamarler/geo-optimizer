import { useState } from 'react';

export default function ContentDisplay({ data }) {
  const [activeTab, setActiveTab] = useState('overview');

  const tabs = [
    { id: 'overview', label: 'Overview', icon: '📊' },
    { id: 'content', label: 'Content', icon: '📄' },
    { id: 'metadata', label: 'Metadata', icon: '🏷️' },
    { id: 'recommendations', label: 'Recommendations', icon: '💡' },
  ];

  return (
    <div className="card max-w-6xl mx-auto">
      {/* Tabs */}
      <div className="border-b border-gray-200 mb-6">
        <nav className="flex space-x-8" aria-label="Tabs">
          {tabs.map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`
                py-4 px-1 border-b-2 font-medium text-sm transition-colors
                ${activeTab === tab.id
                  ? 'border-primary-500 text-primary-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }
              `}
            >
              <span className="mr-2">{tab.icon}</span>
              {tab.label}
            </button>
          ))}
        </nav>
      </div>

      {/* Tab Content */}
      <div className="space-y-6">
        {activeTab === 'overview' && (
          <div className="space-y-6">
            <div>
              <h3 className="text-2xl font-bold text-gray-900 mb-2">{data.title || 'Untitled'}</h3>
              <a href={data.url} target="_blank" rel="noopener noreferrer" className="text-primary-600 hover:underline">
                {data.url}
              </a>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="bg-gray-50 rounded-lg p-4">
                <div className="text-sm text-gray-500 mb-1">Word Count</div>
                <div className="text-2xl font-bold text-gray-900">
                  {data.markdown?.split(' ').length.toLocaleString() || '0'}
                </div>
              </div>
              <div className="bg-gray-50 rounded-lg p-4">
                <div className="text-sm text-gray-500 mb-1">Status</div>
                <div className="text-2xl font-bold text-green-600">
                  {data.success ? 'Success' : 'Failed'}
                </div>
              </div>
              <div className="bg-gray-50 rounded-lg p-4">
                <div className="text-sm text-gray-500 mb-1">Language</div>
                <div className="text-2xl font-bold text-gray-900">
                  {data.language || 'English'}
                </div>
              </div>
            </div>
          </div>
        )}

        {activeTab === 'content' && (
          <div className="space-y-4">
            <div>
              <h4 className="text-lg font-semibold text-gray-900 mb-3">Scraped Content</h4>
              <div className="bg-gray-50 rounded-lg p-6 max-h-96 overflow-y-auto">
                <pre className="whitespace-pre-wrap text-sm text-gray-700 font-mono">
                  {data.markdown || data.content || 'No content available'}
                </pre>
              </div>
            </div>
          </div>
        )}

        {activeTab === 'metadata' && (
          <div className="space-y-4">
            <h4 className="text-lg font-semibold text-gray-900 mb-3">Page Metadata</h4>
            <div className="space-y-3">
              {data.metadata && Object.entries(data.metadata).map(([key, value]) => (
                <div key={key} className="flex border-b border-gray-200 pb-2">
                  <div className="w-1/3 text-sm font-medium text-gray-500">{key}</div>
                  <div className="w-2/3 text-sm text-gray-900 break-words">
                    {typeof value === 'object' ? JSON.stringify(value, null, 2) : String(value)}
                  </div>
                </div>
              ))}
              {!data.metadata && (
                <p className="text-gray-500 italic">No metadata available</p>
              )}
            </div>
          </div>
        )}

        {activeTab === 'recommendations' && (
          <div className="space-y-4">
            <h4 className="text-lg font-semibold text-gray-900 mb-3">GEO Optimization Recommendations</h4>
            <div className="space-y-4">
              <RecommendationCard
                title="Content Structure"
                status="good"
                description="Your content has a clear structure with proper headings."
              />
              <RecommendationCard
                title="Keyword Density"
                status="warning"
                description="Consider adding more relevant keywords to improve discoverability."
              />
              <RecommendationCard
                title="Meta Information"
                status={data.metadata?.description ? 'good' : 'error'}
                description={data.metadata?.description 
                  ? "Good meta description found." 
                  : "Add a meta description to improve GEO performance."}
              />
              <RecommendationCard
                title="Content Length"
                status={data.markdown?.split(' ').length > 300 ? 'good' : 'warning'}
                description={data.markdown?.split(' ').length > 300
                  ? "Content length is sufficient for AI engines."
                  : "Consider adding more detailed content for better optimization."}
              />
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

function RecommendationCard({ title, status, description }) {
  const statusColors = {
    good: 'bg-green-100 text-green-800 border-green-200',
    warning: 'bg-yellow-100 text-yellow-800 border-yellow-200',
    error: 'bg-red-100 text-red-800 border-red-200',
  };

  const statusIcons = {
    good: '✓',
    warning: '⚠',
    error: '✕',
  };

  return (
    <div className={`border rounded-lg p-4 ${statusColors[status]}`}>
      <div className="flex items-start space-x-3">
        <div className="text-2xl">{statusIcons[status]}</div>
        <div>
          <h5 className="font-semibold mb-1">{title}</h5>
          <p className="text-sm opacity-90">{description}</p>
        </div>
      </div>
    </div>
  );
}


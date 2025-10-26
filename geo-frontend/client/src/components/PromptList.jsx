import { useState } from 'react';

export default function PromptList({ prompts, onApprove, onUpdate, onDelete }) {
  const [editingIndex, setEditingIndex] = useState(null);
  const [editedPrompt, setEditedPrompt] = useState(null);

  const categoryColors = {
    informational: 'bg-blue-100 text-blue-800 border-blue-200',
    navigational: 'bg-green-100 text-green-800 border-green-200',
    transactional: 'bg-purple-100 text-purple-800 border-purple-200',
    comparison: 'bg-orange-100 text-orange-800 border-orange-200',
  };

  const categoryIcons = {
    informational: '📖',
    navigational: '🧭',
    transactional: '💳',
    comparison: '⚖️',
  };

  const handleEdit = (index) => {
    setEditingIndex(index);
    setEditedPrompt({ ...prompts[index] });
  };

  const handleSave = (index) => {
    onUpdate(index, editedPrompt);
    setEditingIndex(null);
    setEditedPrompt(null);
  };

  const handleCancel = () => {
    setEditingIndex(null);
    setEditedPrompt(null);
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="text-center space-y-3">
        <h2 className="text-3xl font-bold text-gray-900">Review Test Prompts</h2>
        <p className="text-gray-600">Edit or approve these prompts for GEO testing</p>
      </div>

      {/* Prompts List */}
      <div className="space-y-4 max-w-4xl mx-auto">
        {prompts.map((prompt, index) => (
          <div key={index} className="card hover:shadow-md transition-shadow">
            <div className="flex items-start justify-between space-x-4">
              <div className="flex-1 space-y-3">
                {/* Category Badge */}
                <div className="flex items-center space-x-2">
                  <span className="text-2xl">{categoryIcons[prompt.category] || '💬'}</span>
                  <span className={`text-xs font-medium px-2.5 py-1 rounded-full border ${categoryColors[prompt.category] || 'bg-gray-100 text-gray-800 border-gray-200'}`}>
                    {prompt.category}
                  </span>
                </div>

                {/* Prompt Text */}
                {editingIndex === index ? (
                  <div className="space-y-2">
                    <textarea
                      value={editedPrompt.prompt}
                      onChange={(e) => setEditedPrompt({ ...editedPrompt, prompt: e.target.value })}
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent outline-none resize-none"
                      rows="2"
                    />
                    <input
                      type="text"
                      value={editedPrompt.intent}
                      onChange={(e) => setEditedPrompt({ ...editedPrompt, intent: e.target.value })}
                      placeholder="User intent..."
                      className="w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent outline-none"
                    />
                  </div>
                ) : (
                  <>
                    <p className="text-lg text-gray-900 font-medium">&ldquo;{prompt.prompt}&rdquo;</p>
                    <p className="text-sm text-gray-600 italic">Intent: {prompt.intent}</p>
                  </>
                )}
              </div>

              {/* Action Buttons */}
              <div className="flex space-x-2 flex-shrink-0">
                {editingIndex === index ? (
                  <>
                    <button
                      onClick={() => handleSave(index)}
                      className="p-2 text-green-600 hover:bg-green-50 rounded-lg transition-colors"
                      title="Save"
                    >
                      <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                      </svg>
                    </button>
                    <button
                      onClick={handleCancel}
                      className="p-2 text-gray-600 hover:bg-gray-50 rounded-lg transition-colors"
                      title="Cancel"
                    >
                      <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                      </svg>
                    </button>
                  </>
                ) : (
                  <>
                    <button
                      onClick={() => handleEdit(index)}
                      className="p-2 text-blue-600 hover:bg-blue-50 rounded-lg transition-colors"
                      title="Edit"
                    >
                      <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                      </svg>
                    </button>
                    <button
                      onClick={() => onDelete(index)}
                      className="p-2 text-red-600 hover:bg-red-50 rounded-lg transition-colors"
                      title="Delete"
                    >
                      <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                      </svg>
                    </button>
                  </>
                )}
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Actions */}
      <div className="flex justify-center space-x-4 pt-4">
        <button
          onClick={onApprove}
          disabled={prompts.length === 0}
          className="btn-primary"
        >
          <span className="flex items-center">
            <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
            </svg>
            Approve {prompts.length} Prompt{prompts.length !== 1 ? 's' : ''} & Save
          </span>
        </button>
      </div>
    </div>
  );
}


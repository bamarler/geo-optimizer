import { useState } from 'react';

export default function PersonaCard({ persona, index, onUpdate, onDelete }) {
  const [isEditing, setIsEditing] = useState(false);
  const [editedPersona, setEditedPersona] = useState(persona);

  const handleSave = () => {
    onUpdate(index, editedPersona);
    setIsEditing(false);
  };

  const handleCancel = () => {
    setEditedPersona(persona);
    setIsEditing(false);
  };

  const updateField = (field, value) => {
    setEditedPersona({ ...editedPersona, [field]: value });
  };

  const updateArrayField = (field, arrayIndex, value) => {
    const newArray = [...editedPersona[field]];
    newArray[arrayIndex] = value;
    setEditedPersona({ ...editedPersona, [field]: newArray });
  };

  const addArrayItem = (field) => {
    setEditedPersona({ ...editedPersona, [field]: [...editedPersona[field], ''] });
  };

  const removeArrayItem = (field, arrayIndex) => {
    const newArray = editedPersona[field].filter((_, i) => i !== arrayIndex);
    setEditedPersona({ ...editedPersona, [field]: newArray });
  };

  const colors = [
    'from-blue-500 to-blue-600',
    'from-purple-500 to-purple-600',
    'from-green-500 to-green-600',
    'from-orange-500 to-orange-600',
    'from-pink-500 to-pink-600',
  ];

  const colorClass = colors[index % colors.length];

  return (
    <div className="card hover:shadow-md transition-shadow">
      {/* Header */}
      <div className="flex items-start justify-between mb-4">
        <div className="flex items-center space-x-3">
          <div className={`w-12 h-12 bg-gradient-to-br ${colorClass} rounded-full flex items-center justify-center text-white text-xl font-bold`}>
            {persona.name.charAt(0)}
          </div>
          <div>
            {isEditing ? (
              <input
                type="text"
                value={editedPersona.name}
                onChange={(e) => updateField('name', e.target.value)}
                className="text-xl font-bold border-b-2 border-gray-300 focus:border-primary-500 outline-none"
              />
            ) : (
              <h3 className="text-xl font-bold text-gray-900">{persona.name}</h3>
            )}
            {isEditing ? (
              <input
                type="text"
                value={editedPersona.occupation}
                onChange={(e) => updateField('occupation', e.target.value)}
                className="text-sm text-gray-600 border-b border-gray-300 focus:border-primary-500 outline-none w-full"
              />
            ) : (
              <p className="text-sm text-gray-600">{persona.occupation}</p>
            )}
          </div>
        </div>
        
        <div className="flex space-x-2">
          {isEditing ? (
            <>
              <button
                onClick={handleSave}
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
                onClick={() => setIsEditing(true)}
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

      {/* Details */}
      <div className="space-y-4">
        <div className="flex space-x-4 text-sm">
          <div className="flex items-center space-x-1">
            <span className="text-gray-500">Age:</span>
            {isEditing ? (
              <input
                type="text"
                value={editedPersona.age}
                onChange={(e) => updateField('age', e.target.value)}
                className="border-b border-gray-300 focus:border-primary-500 outline-none w-20"
              />
            ) : (
              <span className="font-medium">{persona.age}</span>
            )}
          </div>
          <div className="flex items-center space-x-1">
            <span className="text-gray-500">Location:</span>
            {isEditing ? (
              <input
                type="text"
                value={editedPersona.location}
                onChange={(e) => updateField('location', e.target.value)}
                className="border-b border-gray-300 focus:border-primary-500 outline-none"
              />
            ) : (
              <span className="font-medium">{persona.location}</span>
            )}
          </div>
        </div>

        {/* Quote */}
        <div className="bg-gray-50 rounded-lg p-3 border-l-4 border-primary-500">
          {isEditing ? (
            <textarea
              value={editedPersona.quote}
              onChange={(e) => updateField('quote', e.target.value)}
              className="w-full bg-transparent italic text-gray-700 outline-none resize-none"
              rows="2"
            />
          ) : (
            <p className="italic text-gray-700">&ldquo;{persona.quote}&rdquo;</p>
          )}
        </div>

        {/* Goals */}
        <div>
          <h4 className="text-sm font-semibold text-gray-900 mb-2 flex items-center">
            <svg className="w-4 h-4 mr-1 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            Goals
          </h4>
          <ul className="space-y-1">
            {isEditing ? (
              <>
                {editedPersona.goals.map((goal, i) => (
                  <li key={i} className="flex items-center space-x-2">
                    <span className="text-gray-400">•</span>
                    <input
                      type="text"
                      value={goal}
                      onChange={(e) => updateArrayField('goals', i, e.target.value)}
                      className="flex-1 text-sm border-b border-gray-300 focus:border-primary-500 outline-none"
                    />
                    <button
                      onClick={() => removeArrayItem('goals', i)}
                      className="text-red-500 hover:text-red-700"
                    >
                      ×
                    </button>
                  </li>
                ))}
                <button
                  onClick={() => addArrayItem('goals')}
                  className="text-sm text-primary-600 hover:text-primary-700"
                >
                  + Add goal
                </button>
              </>
            ) : (
              persona.goals.map((goal, i) => (
                <li key={i} className="text-sm text-gray-700 flex items-start">
                  <span className="text-gray-400 mr-2">•</span>
                  <span>{goal}</span>
                </li>
              ))
            )}
          </ul>
        </div>

        {/* Pain Points */}
        <div>
          <h4 className="text-sm font-semibold text-gray-900 mb-2 flex items-center">
            <svg className="w-4 h-4 mr-1 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            Pain Points
          </h4>
          <ul className="space-y-1">
            {isEditing ? (
              <>
                {editedPersona.painPoints.map((pain, i) => (
                  <li key={i} className="flex items-center space-x-2">
                    <span className="text-gray-400">•</span>
                    <input
                      type="text"
                      value={pain}
                      onChange={(e) => updateArrayField('painPoints', i, e.target.value)}
                      className="flex-1 text-sm border-b border-gray-300 focus:border-primary-500 outline-none"
                    />
                    <button
                      onClick={() => removeArrayItem('painPoints', i)}
                      className="text-red-500 hover:text-red-700"
                    >
                      ×
                    </button>
                  </li>
                ))}
                <button
                  onClick={() => addArrayItem('painPoints')}
                  className="text-sm text-primary-600 hover:text-primary-700"
                >
                  + Add pain point
                </button>
              </>
            ) : (
              persona.painPoints.map((pain, i) => (
                <li key={i} className="text-sm text-gray-700 flex items-start">
                  <span className="text-gray-400 mr-2">•</span>
                  <span>{pain}</span>
                </li>
              ))
            )}
          </ul>
        </div>

        {/* Behavior */}
        <div>
          <h4 className="text-sm font-semibold text-gray-900 mb-2 flex items-center">
            <svg className="w-4 h-4 mr-1 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 8h10M7 12h4m1 8l-4-4H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-3l-4 4z" />
            </svg>
            Behavior
          </h4>
          {isEditing ? (
            <textarea
              value={editedPersona.behavior}
              onChange={(e) => updateField('behavior', e.target.value)}
              className="w-full text-sm text-gray-700 border rounded-lg p-2 outline-none focus:border-primary-500 resize-none"
              rows="2"
            />
          ) : (
            <p className="text-sm text-gray-700">{persona.behavior}</p>
          )}
        </div>
      </div>
    </div>
  );
}


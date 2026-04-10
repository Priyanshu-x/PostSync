import React, { useState } from 'react';
import PostEditor from './components/PostEditor';
import PreviewBoard from './components/PreviewBoard';
import { Sparkles } from 'lucide-react';

const API_BASE_URL = 'http://127.0.0.1:8000';

function App() {
  const [baseText, setBaseText] = useState('');
  const [platforms, setPlatforms] = useState(['twitter', 'linkedin']);
  const [isGenerating, setIsGenerating] = useState(false);
  const [isPublishing, setIsPublishing] = useState(false);
  
  // Previews holds the mapping { platform: caption }
  const [previews, setPreviews] = useState(null);
  
  // idle | success | error
  const [publishStatus, setPublishStatus] = useState('idle');

  const handleGeneratePreviews = async () => {
    setIsGenerating(true);
    setPublishStatus('idle');
    try {
      const res = await fetch(`${API_BASE_URL}/generate-preview`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          base_text: baseText,
          platforms: platforms
        })
      });
      
      if (!res.ok) throw new Error('API Error');
      const data = await res.json();
      setPreviews(data.captions);
    } catch (e) {
      console.error(e);
      alert('Failed to generate previews. Is the backend running?');
    } finally {
      setIsGenerating(false);
    }
  };

  const handlePublish = async () => {
    setIsPublishing(true);
    try {
      const res = await fetch(`${API_BASE_URL}/publish`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          captions: previews,
          platforms: platforms
        })
      });
      
      if (!res.ok) throw new Error('API Error');
      setPublishStatus('success');
    } catch (e) {
      console.error(e);
      setPublishStatus('error');
    } finally {
      setIsPublishing(false);
    }
  };

  return (
    <>
      <header style={{ padding: '2rem 2rem 0', maxWidth: '1200px', margin: '0 auto', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
        <Sparkles color="hsl(var(--accent-primary))" size={32} />
        <h1 style={{ background: 'linear-gradient(to right, white, hsl(var(--text-secondary)))', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent' }}>
          PostSync Engine
        </h1>
      </header>

      <main className="app-container">
        <PostEditor 
          baseText={baseText}
          setBaseText={setBaseText}
          platforms={platforms}
          setPlatforms={setPlatforms}
          onGenerate={handleGeneratePreviews}
          isLoading={isGenerating}
        />
        <PreviewBoard 
          previews={previews}
          setPreviews={setPreviews}
          onPublish={handlePublish}
          isPublishing={isPublishing}
          publishStatus={publishStatus}
        />
      </main>
    </>
  );
}

export default App;

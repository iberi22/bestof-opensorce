import React, { useState, useRef, useEffect } from 'react';
import { Mic, Square, Play, Pause, Upload, Globe, Video, Download } from 'lucide-react';

function VoiceRecorder() {
  const [isRecording, setIsRecording] = useState(false);
  const [audioBlob, setAudioBlob] = useState(null);
  const [audioUrl, setAudioUrl] = useState(null);
  const [isPlaying, setIsPlaying] = useState(false);
  const [script, setScript] = useState('');
  const [selectedLanguages, setSelectedLanguages] = useState(['en', 'es']);
  const [generationStatus, setGenerationStatus] = useState({});

  const mediaRecorderRef = useRef(null);
  const audioRef = useRef(null);
  const chunksRef = useRef([]);

  const languages = [
    { code: 'en', name: 'English', flag: '🇺🇸' },
    { code: 'es', name: 'Español', flag: '🇪🇸' },
    { code: 'fr', name: 'Français', flag: '🇫🇷' },
    { code: 'de', name: 'Deutsch', flag: '🇩🇪' },
    { code: 'it', name: 'Italiano', flag: '🇮🇹' },
    { code: 'pt', name: 'Português', flag: '🇵🇹' },
    { code: 'ru', name: 'Русский', flag: '🇷🇺' },
    { code: 'zh-cn', name: '中文', flag: '🇨🇳' },
    { code: 'ja', name: '日本語', flag: '🇯🇵' },
    { code: 'ar', name: 'العربية', flag: '🇸🇦' },
  ];

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      mediaRecorderRef.current = new MediaRecorder(stream);
      chunksRef.current = [];

      mediaRecorderRef.current.ondataavailable = (e) => {
        if (e.data.size > 0) {
          chunksRef.current.push(e.data);
        }
      };

      mediaRecorderRef.current.onstop = () => {
        const blob = new Blob(chunksRef.current, { type: 'audio/wav' });
        setAudioBlob(blob);
        const url = URL.createObjectURL(blob);
        setAudioUrl(url);
      };

      mediaRecorderRef.current.start();
      setIsRecording(true);
    } catch (error) {
      console.error('Error accessing microphone:', error);
      alert('Error: Could not access microphone');
    }
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current && isRecording) {
      mediaRecorderRef.current.stop();
      mediaRecorderRef.current.stream.getTracks().forEach(track => track.stop());
      setIsRecording(false);
    }
  };

  const togglePlayback = () => {
    if (audioRef.current) {
      if (isPlaying) {
        audioRef.current.pause();
      } else {
        audioRef.current.play();
      }
      setIsPlaying(!isPlaying);
    }
  };

  const toggleLanguage = (langCode) => {
    setSelectedLanguages(prev =>
      prev.includes(langCode)
        ? prev.filter(l => l !== langCode)
        : [...prev, langCode]
    );
  };

  const generateMultilingualReels = async () => {
    if (!audioBlob || !script) {
      alert('Please record your voice and provide a script');
      return;
    }

    setGenerationStatus({ status: 'processing', message: 'Uploading audio and generating reels...' });

    try {
      // Create FormData
      const formData = new FormData();
      formData.append('audio', audioBlob, 'reference_voice.wav');
      formData.append('script', script);
      formData.append('languages', JSON.stringify(selectedLanguages));

      // Send to backend
      const response = await fetch('/api/generate-multilingual-reels', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error('Failed to generate reels');
      }

      const result = await response.json();
      setGenerationStatus({
        status: 'success',
        message: 'Reels generated successfully!',
        results: result
      });

    } catch (error) {
      console.error('Error generating reels:', error);
      setGenerationStatus({
        status: 'error',
        message: 'Failed to generate reels. Please try again.'
      });
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-blue-900 to-gray-900 text-white p-8">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <header className="mb-12 text-center">
          <h1 className="text-5xl font-bold mb-4 bg-gradient-to-r from-blue-400 to-purple-500 bg-clip-text text-transparent">
            🎙️ Multilingual Reel Studio
          </h1>
          <p className="text-xl text-gray-300">
            Record your voice once, generate reels in multiple languages
          </p>
        </header>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Left Column: Voice Recording */}
          <div className="space-y-6">
            {/* Script Input */}
            <div className="bg-gray-800 rounded-2xl p-6 border border-gray-700">
              <h2 className="text-2xl font-semibold mb-4 flex items-center gap-2">
                <Video className="w-6 h-6 text-blue-400" />
                Script (English)
              </h2>
              <textarea
                value={script}
                onChange={(e) => setScript(e.target.value)}
                placeholder="Enter your 20-second script here..."
                className="w-full h-32 bg-gray-900 border border-gray-600 rounded-lg p-4 text-white placeholder-gray-500 focus:border-blue-500 focus:ring-2 focus:ring-blue-500 outline-none resize-none"
              />
              <p className="text-sm text-gray-400 mt-2">
                Word count: {script.split(' ').filter(w => w).length} (~{Math.ceil(script.split(' ').filter(w => w).length / 2.5)} seconds)
              </p>
            </div>

            {/* Voice Recording */}
            <div className="bg-gray-800 rounded-2xl p-6 border border-gray-700">
              <h2 className="text-2xl font-semibold mb-4 flex items-center gap-2">
                <Mic className="w-6 h-6 text-red-400" />
                Voice Recording
              </h2>

              <div className="flex flex-col items-center gap-4">
                {!audioUrl ? (
                  <button
                    onClick={isRecording ? stopRecording : startRecording}
                    className={`w-32 h-32 rounded-full flex items-center justify-center transition-all ${
                      isRecording
                        ? 'bg-red-600 hover:bg-red-700 animate-pulse'
                        : 'bg-blue-600 hover:bg-blue-700'
                    }`}
                  >
                    {isRecording ? (
                      <Square className="w-12 h-12" />
                    ) : (
                      <Mic className="w-12 h-12" />
                    )}
                  </button>
                ) : (
                  <div className="w-full space-y-4">
                    <audio ref={audioRef} src={audioUrl} onEnded={() => setIsPlaying(false)} className="hidden" />
                    <div className="flex items-center gap-4">
                      <button
                        onClick={togglePlayback}
                        className="w-16 h-16 rounded-full bg-green-600 hover:bg-green-700 flex items-center justify-center transition-all"
                      >
                        {isPlaying ? <Pause className="w-8 h-8" /> : <Play className="w-8 h-8 ml-1" />}
                      </button>
                      <div className="flex-1 bg-gray-900 rounded-lg p-4">
                        <p className="text-sm text-gray-400">Recording ready</p>
                        <div className="h-2 bg-gray-700 rounded-full mt-2 overflow-hidden">
                          <div className="h-full bg-gradient-to-r from-blue-500 to-purple-500 w-full"></div>
                        </div>
                      </div>
                    </div>
                    <button
                      onClick={() => {
                        setAudioUrl(null);
                        setAudioBlob(null);
                      }}
                      className="w-full px-4 py-2 bg-gray-700 hover:bg-gray-600 rounded-lg transition-colors"
                    >
                      Record Again
                    </button>
                  </div>
                )}

                <p className="text-sm text-gray-400 text-center">
                  {isRecording ? 'Recording... Click to stop' : audioUrl ? 'Recording saved' : 'Click to start recording'}
                </p>
              </div>
            </div>
          </div>

          {/* Right Column: Language Selection & Generation */}
          <div className="space-y-6">
            {/* Language Selection */}
            <div className="bg-gray-800 rounded-2xl p-6 border border-gray-700">
              <h2 className="text-2xl font-semibold mb-4 flex items-center gap-2">
                <Globe className="w-6 h-6 text-green-400" />
                Target Languages
              </h2>

              <div className="grid grid-cols-2 gap-3">
                {languages.map((lang) => (
                  <button
                    key={lang.code}
                    onClick={() => toggleLanguage(lang.code)}
                    className={`p-4 rounded-lg border-2 transition-all ${
                      selectedLanguages.includes(lang.code)
                        ? 'border-blue-500 bg-blue-900/30'
                        : 'border-gray-600 bg-gray-900/30 hover:border-gray-500'
                    }`}
                  >
                    <div className="text-3xl mb-1">{lang.flag}</div>
                    <div className="text-sm font-medium">{lang.name}</div>
                  </button>
                ))}
              </div>

              <p className="text-sm text-gray-400 mt-4">
                Selected: {selectedLanguages.length} language{selectedLanguages.length !== 1 ? 's' : ''}
              </p>
            </div>

            {/* Generate Button */}
            <button
              onClick={generateMultilingualReels}
              disabled={!audioBlob || !script || selectedLanguages.length === 0}
              className="w-full py-6 bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 rounded-2xl font-bold text-xl transition-all disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-3"
            >
              <Video className="w-6 h-6" />
              Generate Multilingual Reels
            </button>

            {/* Status */}
            {generationStatus.status && (
              <div className={`p-6 rounded-2xl border-2 ${
                generationStatus.status === 'success' ? 'border-green-500 bg-green-900/20' :
                generationStatus.status === 'error' ? 'border-red-500 bg-red-900/20' :
                'border-blue-500 bg-blue-900/20'
              }`}>
                <p className="font-semibold mb-2">{generationStatus.message}</p>

                {generationStatus.results && (
                  <div className="mt-4 space-y-2">
                    {Object.entries(generationStatus.results).map(([lang, path]) => (
                      <div key={lang} className="flex items-center justify-between bg-gray-900/50 p-3 rounded-lg">
                        <span className="flex items-center gap-2">
                          {languages.find(l => l.code === lang)?.flag} {lang.toUpperCase()}
                        </span>
                        <button className="px-3 py-1 bg-blue-600 hover:bg-blue-700 rounded-lg text-sm flex items-center gap-2">
                          <Download className="w-4 h-4" />
                          Download
                        </button>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

export default VoiceRecorder;

document.addEventListener('DOMContentLoaded', () => {
    const uploadZone = document.getElementById('upload-zone');
    const imageUpload = document.getElementById('image-upload');
    const previewImg = document.getElementById('preview-img');
    const previewPlaceholder = document.getElementById('preview-placeholder');
    
    // UI Elements to update
    const primaryPredictionText = document.getElementById('primary-prediction-text');
    const primaryConfidenceText = document.getElementById('primary-confidence-text');
    const primaryConfidenceLabel = document.getElementById('primary-confidence-label');
    const primaryResultCard = document.getElementById('primary-result-card');
    const confidenceBarsContainer = document.getElementById('confidence-bars-container');
    const aiInsightText = document.getElementById('ai-insight-text');
    const rawTensorsBody = document.getElementById('raw-tensors-body');
    
    // Drag and Drop events
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        uploadZone.addEventListener(eventName, preventDefaults, false);
    });
    
    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }
    
    ['dragenter', 'dragover'].forEach(eventName => {
        uploadZone.addEventListener(eventName, () => {
            uploadZone.classList.add('bg-surface-container');
        }, false);
    });
    
    ['dragleave', 'drop'].forEach(eventName => {
        uploadZone.addEventListener(eventName, () => {
            uploadZone.classList.remove('bg-surface-container');
        }, false);
    });
    
    uploadZone.addEventListener('drop', (e) => {
        const dt = e.dataTransfer;
        const files = dt.files;
        if (files.length > 0) {
            handleFile(files[0]);
        }
    }, false);
    
    imageUpload.addEventListener('change', function() {
        if (this.files && this.files.length > 0) {
            handleFile(this.files[0]);
        }
    });
    
    function handleFile(file) {
        if (!file.type.startsWith('image/')) {
            alert('Please upload an image file (JPG, PNG).');
            return;
        }
        
        // Update text
        document.getElementById('upload-text').innerText = 'Image Selected';
        document.getElementById('upload-subtext').innerText = file.name;
        
        // Show local preview
        const reader = new FileReader();
        reader.onload = (e) => {
            previewImg.src = e.target.result;
            previewImg.style.display = 'block';
            previewPlaceholder.style.display = 'none';
        }
        reader.readAsDataURL(file);
        
        // Reset UI state to loading
        primaryPredictionText.innerText = 'Analyzing...';
        primaryConfidenceText.innerText = '--%';
        primaryConfidenceLabel.innerText = 'Processing';
        confidenceBarsContainer.innerHTML = '<div class="text-on-surface-variant font-medium text-sm animate-pulse">Running neural network...</div>';
        
        // Upload and Predict
        const formData = new FormData();
        formData.append('file', file);
        
        fetch('/predict', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert("Error: " + data.error);
                return;
            }
            updateUI(data);
        })
        .catch(error => {
            console.error('Error:', error);
            alert("An error occurred while making the prediction.");
        });
    }
    
    function updateUI(data) {
        // Primary Card
        primaryPredictionText.innerText = data.predicted_class;
        primaryConfidenceText.innerText = data.confidence.toFixed(1) + '%';
        primaryConfidenceLabel.innerText = data.confidence_level + ' Confidence';
        
        // Card Color
        primaryResultCard.classList.remove('bg-surface', 'bg-[#22C55E]', 'bg-[#3B82F6]', 'bg-[#F97316]');
        if (data.confidence >= 90) {
            primaryResultCard.classList.add('bg-[#22C55E]'); // Green
            primaryConfidenceLabel.className = 'bg-primary text-[#22C55E] font-headline text-xs font-bold uppercase px-3 py-1 mt-2 inline-block border-2 border-primary';
        } else if (data.confidence >= 70) {
            primaryResultCard.classList.add('bg-[#3B82F6]'); // Blue
            primaryConfidenceLabel.className = 'bg-primary text-[#3B82F6] font-headline text-xs font-bold uppercase px-3 py-1 mt-2 inline-block border-2 border-primary';
        } else {
            primaryResultCard.classList.add('bg-[#F97316]'); // Orange
            primaryConfidenceLabel.className = 'bg-primary text-[#F97316] font-headline text-xs font-bold uppercase px-3 py-1 mt-2 inline-block border-2 border-primary';
        }
        
        // Confidence Bars
        confidenceBarsContainer.innerHTML = '';
        data.all_scores.forEach((item, index) => {
            const isTop = index === 0;
            const barColor = isTop ? (data.confidence >= 90 ? 'bg-[#22C55E]' : (data.confidence >= 70 ? 'bg-[#3B82F6]' : 'bg-[#F97316]')) : 'bg-primary';
            const html = `
                <div>
                    <div class="flex justify-between font-headline font-bold uppercase text-sm mb-2">
                        <span>${item.label}</span>
                        <span class="${!isTop ? 'text-on-surface-variant' : ''}">${item.score.toFixed(1)}%</span>
                    </div>
                    <div class="h-8 w-full border-4 border-primary bg-surface-container relative overflow-hidden">
                        <div class="absolute top-0 left-0 h-full ${barColor} progress-bar-fill ${isTop ? 'border-r-4 border-primary' : ''}" style="width: 0%;" id="bar-${item.id}"></div>
                    </div>
                </div>
            `;
            confidenceBarsContainer.insertAdjacentHTML('beforeend', html);
            
            // Animate bar
            setTimeout(() => {
                document.getElementById(`bar-${item.id}`).style.width = `${item.score}%`;
            }, 50);
        });
        
        // AI Insight
        aiInsightText.innerHTML = data.insight.replace(data.predicted_class, `<span class="font-bold uppercase ${data.confidence >= 90 ? 'text-[#22C55E]' : (data.confidence >= 70 ? 'text-[#3B82F6]' : 'text-[#F97316]')} bg-primary px-2 py-0.5">${data.predicted_class}</span>`);
        
        // Raw Data Table
        rawTensorsBody.innerHTML = '';
        data.all_scores.forEach(item => {
            const isPredicted = item.id === data.predicted_index;
            let trClass = 'border-b-4 border-primary';
            let tdClass = 'font-bold';
            
            if (isPredicted) {
                if (data.confidence >= 90) trClass += ' bg-[#22C55E]';
                else if (data.confidence >= 70) trClass += ' bg-[#3B82F6]';
                else trClass += ' bg-[#F97316]';
                tdClass = 'font-black';
            }
            
            const html = `
                <tr class="${trClass}">
                    <td class="p-3 border-r-4 border-primary ${tdClass}">${item.id}</td>
                    <td class="p-3 border-r-4 border-primary ${tdClass}">${item.label}</td>
                    <td class="p-3 text-right font-mono ${tdClass}">${item.raw_value.toFixed(6)}</td>
                </tr>
            `;
            rawTensorsBody.insertAdjacentHTML('beforeend', html);
        });
    }
});

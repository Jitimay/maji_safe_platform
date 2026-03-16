/**
 * MajiSafe Cyberpunk Platform Frontend
 * Enhanced cyberpunk interface with advanced features
 */

class CyberMajiSafeApp {
    constructor() {
        this.socket = null;
        this.demandChart = null;
        this.apiBase = '';
        this.currentSection = 'dashboard';
        this.init();
    }

    init() {
        this.initWebSocket();
        this.initNavigation();
        this.initTimeDisplay();
        this.initSystemMetrics();
        this.initDemandChart();
        this.setupEventListeners();
        this.loadInitialData();
        this.startPeriodicUpdates();
        this.loadSettings();
        
        console.log('🚀 MajiSafe Cyberpunk Platform initialized');
    }

    initWebSocket() {
        this.socket = io();
        
        this.socket.on('connect', () => {
            console.log('🔗 Connected to MajiSafe server');
            this.updateSystemStatus('online');
        });
        
        this.socket.on('disconnect', () => {
            console.log('❌ Disconnected from MajiSafe server');
            this.updateSystemStatus('offline');
        });
        
        this.socket.on('dashboard_update', (data) => {
            this.updateDashboard(data);
        });
        
        this.socket.on('pump_status_change', (data) => {
            this.updatePumpStatus(data);
        });
        
        this.socket.on('demand_update', (data) => {
            this.updateDemandChart(data);
        });
    }

    initNavigation() {
        const navItems = document.querySelectorAll('.nav-item');
        navItems.forEach(item => {
            item.addEventListener('click', () => {
                const section = item.dataset.section;
                this.switchSection(section);
            });
        });
    }

    switchSection(sectionId) {
        // Update nav active state
        document.querySelectorAll('.nav-item').forEach(item => {
            item.classList.remove('active');
        });
        document.querySelector(`[data-section="${sectionId}"]`).classList.add('active');
        
        // Update content sections
        document.querySelectorAll('.content-section').forEach(section => {
            section.classList.remove('active');
        });
        document.getElementById(sectionId).classList.add('active');
        
        this.currentSection = sectionId;
        this.onSectionChange(sectionId);
    }

    onSectionChange(sectionId) {
        switch(sectionId) {
            case 'monitoring':
                this.loadDemandData();
                break;
            case 'analytics':
                this.loadImpactMetrics();
                break;
            case 'network':
                this.updateNetworkMap();
                break;
            case 'alerts':
                this.loadAlerts();
                break;
            case 'ai-thinking':
                this.loadAIThinking();
                break;
            case 'settings':
                this.loadSettings();
                break;
        }
    }

    initTimeDisplay() {
        this.updateTimeDisplay();
        setInterval(() => this.updateTimeDisplay(), 1000);
    }

    updateTimeDisplay() {
        const now = new Date();
        const timeStr = now.toLocaleTimeString('en-US', { 
            hour12: false, 
            hour: '2-digit', 
            minute: '2-digit', 
            second: '2-digit' 
        });
        const dateStr = now.toLocaleDateString('en-US', { 
            year: 'numeric', 
            month: 'short', 
            day: '2-digit' 
        });
        
        document.getElementById('current-time').textContent = timeStr;
        document.getElementById('current-date').textContent = dateStr;
    }

    initSystemMetrics() {
        // Simulate system metrics
        setInterval(() => {
            document.getElementById('cpu-usage').textContent = `${Math.floor(Math.random() * 30 + 40)}%`;
            document.getElementById('mem-usage').textContent = `${Math.floor(Math.random() * 20 + 60)}%`;
            document.getElementById('net-status').textContent = Math.random() > 0.1 ? 'STABLE' : 'UNSTABLE';
        }, 5000);
    }

    updateSystemStatus(status) {
        const indicator = document.querySelector('.status-indicator');
        const statusText = document.querySelector('.system-status span');
        
        if (status === 'online') {
            indicator.style.background = 'var(--cyber-success)';
            indicator.style.boxShadow = 'var(--cyber-glow) var(--cyber-success)';
            statusText.textContent = 'SYSTEM ONLINE';
        } else {
            indicator.style.background = 'var(--cyber-danger)';
            indicator.style.boxShadow = 'var(--cyber-glow) var(--cyber-danger)';
            statusText.textContent = 'SYSTEM OFFLINE';
        }
    }

    initDemandChart() {
        const ctx = document.getElementById('demand-chart').getContext('2d');
        this.demandChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: ['VILLAGE ALPHA', 'VILLAGE BETA'],
                datasets: [{
                    label: 'Water Requests',
                    data: [0, 0],
                    backgroundColor: [
                        'rgba(0, 255, 255, 0.6)',
                        'rgba(255, 0, 128, 0.6)'
                    ],
                    borderColor: [
                        'var(--cyber-primary)',
                        'var(--cyber-secondary)'
                    ],
                    borderWidth: 2,
                    borderRadius: 4,
                    borderSkipped: false,
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: false },
                    title: {
                        display: true,
                        text: 'REAL-TIME DEMAND ANALYSIS',
                        color: 'var(--cyber-primary)',
                        font: { family: 'Orbitron', size: 14 }
                    }
                },
                scales: {
                    x: {
                        ticks: { color: 'var(--cyber-text-dim)' },
                        grid: { color: 'rgba(0, 255, 255, 0.1)' }
                    },
                    y: {
                        beginAtZero: true,
                        ticks: { 
                            color: 'var(--cyber-text-dim)',
                            stepSize: 1 
                        },
                        grid: { color: 'rgba(0, 255, 255, 0.1)' }
                    }
                },
                animation: {
                    duration: 1000,
                    easing: 'easeInOutCubic'
                }
            }
        });
    }

    setupEventListeners() {
        // Pump control buttons
        document.getElementById('start-pump-a')?.addEventListener('click', () => {
            this.controlPump(1, 'start');
        });
        
        document.getElementById('stop-pump-a')?.addEventListener('click', () => {
            this.controlPump(1, 'stop');
        });
        
        document.getElementById('start-pump-b')?.addEventListener('click', () => {
            this.controlPump(2, 'start');
        });
        
        document.getElementById('stop-pump-b')?.addEventListener('click', () => {
            this.controlPump(2, 'stop');
        });
        
        // SMS request simulation
        document.getElementById('request-village-a')?.addEventListener('click', () => {
            this.simulateSMSRequest('village-a');
        });
        
        document.getElementById('request-village-b')?.addEventListener('click', () => {
            this.simulateSMSRequest('village-b');
        });

        // Header controls
        document.getElementById('refresh-data')?.addEventListener('click', () => {
            this.refreshAllData();
        });

        document.getElementById('export-data')?.addEventListener('click', () => {
            this.exportData();
        });

        // Settings controls
        document.getElementById('save-settings')?.addEventListener('click', () => {
            this.saveSettings();
        });

        document.getElementById('reset-settings')?.addEventListener('click', () => {
            this.resetSettings();
        });

        document.getElementById('export-settings')?.addEventListener('click', () => {
            this.exportSettings();
        });

        document.getElementById('refresh-interval')?.addEventListener('change', (e) => {
            this.updateRefreshInterval(parseInt(e.target.value));
        });

        document.getElementById('theme-mode')?.addEventListener('change', (e) => {
            this.changeTheme(e.target.value);
        });

        // Chart period controls
        document.querySelectorAll('.chart-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                document.querySelectorAll('.chart-btn').forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                this.updateChartPeriod(btn.dataset.period);
            });
        });
    }

    loadInitialData() {
        this.loadDashboardData();
        this.loadDemandData();
        this.loadImpactMetrics();
        this.loadActivityLog();
        this.updateNetworkMap();
    }

    startPeriodicUpdates() {
        setInterval(() => this.loadDashboardData(), 5000);
        setInterval(() => this.loadImpactMetrics(), 10000);
        setInterval(() => this.loadActivityLog(), 15000);
        setInterval(() => this.updateNetworkStats(), 8000);
    }

    async loadDashboardData() {
        try {
            const response = await fetch(`${this.apiBase}/api/dashboard/metrics`);
            const data = await response.json();
            
            if (data.error) {
                console.error('Error loading dashboard data:', data.error);
                return;
            }
            
            this.updateDashboard(data);
            
        } catch (error) {
            console.error('Error loading dashboard data:', error);
        }
    }

    async loadDemandData() {
        try {
            const response = await fetch(`${this.apiBase}/api/demand/villages`);
            const data = await response.json();
            
            if (data.error) {
                console.error('Error loading demand data:', data.error);
                return;
            }
            
            this.updateDemandChart(data);
            
        } catch (error) {
            console.error('Error loading demand data:', error);
        }
    }

    updateDashboard(data) {
        // Update metric cards with cyberpunk styling
        document.getElementById('total-water').textContent = `${Math.round(data.total_water_distributed)} L`;
        document.getElementById('current-requests').textContent = data.current_requests;
        document.getElementById('communities-served').textContent = data.communities_served;
        
        // Update pump status with enhanced indicators
        if (data.pump_statuses) {
            data.pump_statuses.forEach(pump => {
                this.updatePumpIndicator(pump);
            });
        }
        
        this.updateNetworkMap();
    }

    updatePumpIndicator(pump) {
        const pumpId = pump.pump_id.replace('pump-', '');
        const statusElement = document.getElementById(`pump-${pumpId}-status`);
        const indicatorElement = document.getElementById(`pump-${pumpId}-indicator`);
        const runtimeElement = document.getElementById(`runtime-${pumpId}`);
        const cardElement = document.getElementById(`pump-${pumpId === 'a' ? '1' : '2'}-card`);
        
        if (statusElement) {
            statusElement.textContent = pump.status === 'ON' ? 'ONLINE' : 'OFFLINE';
        }
        
        if (indicatorElement) {
            const statusLight = indicatorElement.querySelector('.status-light');
            if (pump.status === 'ON') {
                statusLight.classList.add('on');
                statusLight.classList.remove('off');
            } else {
                statusLight.classList.add('off');
                statusLight.classList.remove('on');
            }
        }
        
        if (runtimeElement && pump.runtime_minutes !== undefined) {
            runtimeElement.textContent = `${pump.runtime_minutes}m`;
        }
        
        // Update pump card styling
        if (cardElement) {
            if (pump.status === 'ON') {
                cardElement.style.borderColor = 'var(--cyber-success)';
                cardElement.style.boxShadow = '0 0 20px rgba(0, 255, 0, 0.3)';
            } else {
                cardElement.style.borderColor = 'var(--cyber-border)';
                cardElement.style.boxShadow = 'none';
            }
        }
    }

    updateNetworkMap() {
        // Update SVG pump nodes based on status
        const pumpAStatus = document.getElementById('pump-a-status')?.textContent;
        const pumpBStatus = document.getElementById('pump-b-status')?.textContent;
        
        const pump1Node = document.getElementById('pump-1-node');
        const pump2Node = document.getElementById('pump-2-node');
        
        if (pump1Node) {
            if (pumpAStatus === 'ONLINE') {
                pump1Node.classList.add('active');
            } else {
                pump1Node.classList.remove('active');
            }
        }
        
        if (pump2Node) {
            if (pumpBStatus === 'ONLINE') {
                pump2Node.classList.add('active');
            } else {
                pump2Node.classList.remove('active');
            }
        }
    }

    updateNetworkStats() {
        // Simulate network statistics
        const latency = Math.floor(Math.random() * 20 + 5);
        const throughput = (Math.random() * 2 + 1.5).toFixed(1);
        
        document.querySelector('.network-stats .stat-item:nth-child(1) .stat-value').textContent = `${latency}ms`;
        document.querySelector('.network-stats .stat-item:nth-child(2) .stat-value').textContent = `${throughput} MB/s`;
    }

    async controlPump(pumpId, action) {
        try {
            // Add AI thinking
            this.addAIThought(`Received ${action} command for Pump ${pumpId === 1 ? 'Alpha-01' : 'Beta-02'}`);
            this.addAIThought(`Analyzing pump status and system conditions...`);
            
            // Add visual feedback
            const button = document.getElementById(`${action}-pump-${pumpId === 1 ? 'a' : 'b'}`);
            button.style.opacity = '0.6';
            button.disabled = true;
            
            const response = await fetch(`${this.apiBase}/api/pumps/${pumpId}/${action}`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' }
            });
            
            const data = await response.json();
            
            if (data.error) {
                this.addAIThought(`Error detected: ${data.error}`);
                this.showNotification(`Error: ${data.error}`, 'error');
                return;
            }
            
            if (data.status === 'success') {
                this.addAIThought(`Pump ${pumpId === 1 ? 'Alpha-01' : 'Beta-02'} ${action}ed successfully`);
                this.addAIThought(`System status updated - monitoring performance`);
                this.showNotification(`PUMP ${pumpId === 1 ? 'ALPHA' : 'BETA'} ${action.toUpperCase()}ED`, 'success');
                this.updateNetworkMap();
                this.addActivityLogEntry(`PUMP_${action.toUpperCase()}`, `Pump ${pumpId === 1 ? 'Alpha' : 'Beta'} ${action}ed successfully`);
            }
            
        } catch (error) {
            console.error(`Error controlling pump ${pumpId}:`, error);
            this.addAIThought(`System error: Failed to ${action} pump ${pumpId}`);
            this.showNotification(`Failed to ${action} pump ${pumpId}`, 'error');
        } finally {
            // Restore button
            setTimeout(() => {
                const button = document.getElementById(`${action}-pump-${pumpId === 1 ? 'a' : 'b'}`);
                button.style.opacity = '1';
                button.disabled = false;
            }, 1000);
        }
    }

    async loadImpactMetrics() {
        try {
            const response = await fetch(`${this.apiBase}/api/impact/metrics`);
            const data = await response.json();
            
            if (data.error) {
                console.error('Error loading impact metrics:', data.error);
                return;
            }
            
            // Update impact cards
            document.getElementById('impact-water').textContent = `${Math.round(data.total_water_distributed)} L`;
            document.getElementById('impact-people').textContent = data.people_served;
            document.getElementById('impact-communities').textContent = data.communities_served;
            
        } catch (error) {
            console.error('Error loading impact metrics:', error);
        }
    }

    async loadActivityLog() {
        try {
            const response = await fetch(`${this.apiBase}/api/activity/log`);
            const data = await response.json();
            
            if (data.error) {
                console.error('Error loading activity log:', data.error);
                return;
            }
            
            const logContainer = document.getElementById('activity-log');
            logContainer.innerHTML = '';
            
            if (data.log && data.log.length > 0) {
                data.log.forEach(entry => {
                    const item = document.createElement('div');
                    item.className = 'activity-item';
                    
                    // Add specific class based on event type
                    if (entry.event_type.includes('PUMP')) {
                        item.classList.add('pump-event');
                    } else if (entry.event_type.includes('SMS')) {
                        item.classList.add('sms-event');
                    } else if (entry.event_type.includes('DISTRIBUTION')) {
                        item.classList.add('distribution-event');
                    }
                    
                    const time = new Date(entry.timestamp).toLocaleTimeString();
                    const date = new Date(entry.timestamp).toLocaleDateString();
                    
                    item.innerHTML = `
                        <span class="activity-time">${date} ${time}</span>
                        <span class="activity-desc">${entry.description}</span>
                    `;
                    
                    logContainer.appendChild(item);
                });
            } else {
                logContainer.innerHTML = '<div class="activity-item"><span class="activity-desc">No activity logged yet</span></div>';
            }
            
        } catch (error) {
            console.error('Error loading activity log:', error);
        }
    }

    updateSystemMap() {
        // Update pump indicators on the map based on status
        const pumpAStatus = document.getElementById('pump-a-status');
        const pumpBStatus = document.getElementById('pump-b-status');
        
        const pump1Indicator = document.getElementById('pump-1-indicator');
        const pump2Indicator = document.getElementById('pump-2-indicator');
        
        if (pumpAStatus && pump1Indicator) {
            const isOn = pumpAStatus.textContent === 'ON';
            pump1Indicator.setAttribute('fill', isOn ? '#27ae60' : '#e74c3c');
            pump1Indicator.setAttribute('stroke', isOn ? '#229954' : '#c0392b');
        }
        
        if (pumpBStatus && pump2Indicator) {
            const isOn = pumpBStatus.textContent === 'ON';
            pump2Indicator.setAttribute('fill', isOn ? '#27ae60' : '#e74c3c');
            pump2Indicator.setAttribute('stroke', isOn ? '#229954' : '#c0392b');
        }
    }

    updatePumpStatus(data) {
        const pumpIdFormatted = data.pump_id.replace('_', '-');
        const statusElement = document.getElementById(`${pumpIdFormatted}-status`);
        if (statusElement) {
            statusElement.textContent = data.status;
            statusElement.className = `status-badge ${data.status.toLowerCase()}`;
        }
        
        console.log(`Pump ${data.pump_id} status changed to ${data.status}`);
        
        // Reload dashboard to get updated metrics
        this.loadDashboardData();
        this.updateSystemMap();
    }

    updateDemandChart(data) {
        if (this.demandChart) {
            const villageA = data.village_a || { requests: 0 };
            const villageB = data.village_b || { requests: 0 };
            
            this.demandChart.data.datasets[0].data = [
                villageA.requests,
                villageB.requests
            ];
            this.demandChart.update();
            
            // Update current requests total
            const totalRequests = villageA.requests + villageB.requests;
            document.getElementById('current-requests').textContent = totalRequests;
        }
    }

    async controlPump(pumpId, action) {
        try {
            const response = await fetch(`${this.apiBase}/api/pumps/${pumpId}/${action}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                }
            });
            
            const data = await response.json();
            
            if (data.error) {
                this.showNotification(`Error: ${data.error}`, 'error');
                return;
            }
            
            if (data.status === 'success') {
                this.showNotification(`Pump ${pumpId} ${action}ed successfully`);
                // Dashboard will update via WebSocket or next poll
                this.updateSystemMap();
                this.loadActivityLog();
            }
            
        } catch (error) {
            console.error(`Error controlling pump ${pumpId}:`, error);
            this.showNotification(`Failed to ${action} pump ${pumpId}`, 'error');
        }
    }

    async simulateSMSRequest(villageId) {
        try {
            this.addAIThought(`SMS request received from ${villageId.toUpperCase()}`);
            this.addAIThought(`Analyzing message content and urgency level...`);
            this.addAIThought(`Classification: Water request - Medium priority`);
            
            const response = await fetch(`${this.apiBase}/api/sms/request/${villageId}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                }
            });
            
            const data = await response.json();
            
            if (data.error) {
                this.addAIThought(`Error processing SMS: ${data.error}`);
                this.showNotification(`Error: ${data.error}`, 'error');
                return;
            }
            
            if (data.status === 'success') {
                this.addAIThought(`Request logged for ${data.village}`);
                this.addAIThought(`Updating demand analysis and recommendations...`);
                this.showNotification(`Water request added for ${data.village}`);
                // Reload demand data
                this.loadDemandData();
                this.loadDashboardData();
                this.loadActivityLog();
            }
            
        } catch (error) {
            console.error(`Error simulating SMS request for ${villageId}:`, error);
            this.showNotification(`Failed to add request for ${villageId}`, 'error');
        }
    }

    showNotification(message, type = 'success') {
        const notification = document.createElement('div');
        notification.className = `notification ${type}`;
        notification.innerHTML = `
            <i class="fas fa-${type === 'error' ? 'exclamation-triangle' : type === 'success' ? 'check-circle' : 'info-circle'}"></i>
            <span>${message}</span>
        `;
        
        document.body.appendChild(notification);
        
        setTimeout(() => {
            notification.style.animation = 'slideOutRight 0.3s ease';
            setTimeout(() => notification.remove(), 300);
        }, 3000);
    }

    addActivityLogEntry(type, message) {
        const logContainer = document.getElementById('activity-log');
        const timestamp = new Date().toISOString().replace('T', ' ').substring(0, 19);
        
        const logLine = document.createElement('div');
        logLine.className = 'log-line';
        logLine.innerHTML = `
            <span class="timestamp">[${timestamp}]</span>
            <span class="log-level ${type.toLowerCase().includes('error') ? 'error' : type.toLowerCase().includes('warning') ? 'warning' : 'info'}">[${type}]</span>
            <span class="log-message">${message}</span>
        `;
        
        logContainer.insertBefore(logLine, logContainer.firstChild);
        
        // Keep only last 50 entries
        while (logContainer.children.length > 50) {
            logContainer.removeChild(logContainer.lastChild);
        }
    }

    refreshAllData() {
        this.showNotification('REFRESHING ALL DATA...', 'info');
        this.loadDashboardData();
        this.loadDemandData();
        this.loadImpactMetrics();
        this.loadActivityLog();
        this.updateNetworkMap();
    }

    exportData() {
        this.showNotification('DATA EXPORT INITIATED...', 'info');
        // Simulate data export
        setTimeout(() => {
            this.showNotification('DATA EXPORTED SUCCESSFULLY', 'success');
        }, 2000);
    }

    updateChartPeriod(period) {
        this.showNotification(`CHART PERIOD: ${period.toUpperCase()}`, 'info');
        // Simulate chart data update for different periods
        this.loadDemandData();
    }

    loadAlerts() {
        // Simulate loading alerts - in real implementation, this would fetch from API
        this.showNotification('ALERTS LOADED', 'info');
    }

    loadAIThinking() {
        this.startAIThinking();
        this.updateDecisionMatrix();
    }

    startAIThinking() {
        const thinkingContent = document.getElementById('ai-thinking-content');
        if (!thinkingContent) return;

        // Simulate AI thinking process
        const thoughts = [
            "Analyzing incoming SMS requests...",
            "Pattern recognition: Water demand spike detected",
            "Village A: 7 requests, Village B: 3 requests", 
            "Urgency classification: HIGH priority",
            "Checking pump availability and status",
            "Calculating optimal water distribution",
            "Decision: Activate Pump Alpha-01 immediately",
            "Scheduling Pump Beta-02 for 15-minute delay",
            "Confidence level: 94% - Action recommended"
        ];

        let thoughtIndex = 0;
        
        const addThought = () => {
            if (thoughtIndex < thoughts.length) {
                const timestamp = new Date().toLocaleTimeString();
                const thoughtLine = document.createElement('div');
                thoughtLine.className = 'thought-line';
                thoughtLine.innerHTML = `
                    <span class="timestamp">[${timestamp}]</span>
                    <span class="thought">${thoughts[thoughtIndex]}</span>
                `;
                
                thinkingContent.appendChild(thoughtLine);
                thinkingContent.scrollTop = thinkingContent.scrollHeight;
                
                thoughtIndex++;
                setTimeout(addThought, 1500);
            } else {
                // Restart thinking cycle
                setTimeout(() => {
                    thinkingContent.innerHTML = '';
                    thoughtIndex = 0;
                    addThought();
                }, 5000);
            }
        };

        addThought();
    }

    updateDecisionMatrix() {
        // Simulate dynamic decision factors
        setInterval(() => {
            const factors = document.querySelectorAll('.factor-fill');
            factors.forEach(factor => {
                const randomWidth = Math.floor(Math.random() * 40 + 50);
                factor.style.width = `${randomWidth}%`;
            });
        }, 3000);
    }

    addAIThought(message) {
        const thinkingContent = document.getElementById('ai-thinking-content');
        if (!thinkingContent) return;

        const timestamp = new Date().toLocaleTimeString();
        const thoughtLine = document.createElement('div');
        thoughtLine.className = 'thought-line';
        thoughtLine.innerHTML = `
            <span class="timestamp">[${timestamp}]</span>
            <span class="thought">${message}</span>
        `;
        
        thinkingContent.appendChild(thoughtLine);
        thinkingContent.scrollTop = thinkingContent.scrollHeight;

        // Keep only last 20 thoughts
        while (thinkingContent.children.length > 20) {
            thinkingContent.removeChild(thinkingContent.firstChild);
        }
    }

    // Settings Management
    saveSettings() {
        const settings = {
            refreshInterval: document.getElementById('refresh-interval').value,
            themeMode: document.getElementById('theme-mode').value,
            soundAlerts: document.getElementById('sound-alerts').checked,
            flowRate: document.getElementById('flow-rate').value,
            autoShutdown: document.getElementById('auto-shutdown').value,
            pressureThreshold: document.getElementById('pressure-threshold').value
        };
        
        localStorage.setItem('majisafe-settings', JSON.stringify(settings));
        this.showNotification('SETTINGS SAVED SUCCESSFULLY', 'success');
    }

    resetSettings() {
        document.getElementById('refresh-interval').value = '5000';
        document.getElementById('theme-mode').value = 'cyberpunk';
        document.getElementById('sound-alerts').checked = true;
        document.getElementById('flow-rate').value = '20';
        document.getElementById('auto-shutdown').value = '60';
        document.getElementById('pressure-threshold').value = '1.5';
        
        this.showNotification('SETTINGS RESET TO DEFAULT', 'info');
    }

    exportSettings() {
        const settings = {
            refreshInterval: document.getElementById('refresh-interval').value,
            themeMode: document.getElementById('theme-mode').value,
            soundAlerts: document.getElementById('sound-alerts').checked,
            flowRate: document.getElementById('flow-rate').value,
            autoShutdown: document.getElementById('auto-shutdown').value,
            pressureThreshold: document.getElementById('pressure-threshold').value,
            exportDate: new Date().toISOString()
        };
        
        const blob = new Blob([JSON.stringify(settings, null, 2)], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'majisafe-settings.json';
        a.click();
        URL.revokeObjectURL(url);
        
        this.showNotification('SETTINGS EXPORTED', 'success');
    }

    updateRefreshInterval(interval) {
        clearInterval(this.refreshTimer);
        this.refreshTimer = setInterval(() => this.loadDashboardData(), interval);
        this.showNotification(`REFRESH INTERVAL: ${interval/1000}s`, 'info');
    }

    changeTheme(theme) {
        document.body.className = `theme-${theme}`;
        this.showNotification(`THEME CHANGED: ${theme.toUpperCase()}`, 'info');
    }

    loadSettings() {
        const saved = localStorage.getItem('majisafe-settings');
        if (saved) {
            const settings = JSON.parse(saved);
            document.getElementById('refresh-interval').value = settings.refreshInterval || '5000';
            document.getElementById('theme-mode').value = settings.themeMode || 'cyberpunk';
            document.getElementById('sound-alerts').checked = settings.soundAlerts !== false;
            document.getElementById('flow-rate').value = settings.flowRate || '20';
            document.getElementById('auto-shutdown').value = settings.autoShutdown || '60';
            document.getElementById('pressure-threshold').value = settings.pressureThreshold || '1.5';
        }
    }
}

// Initialize the cyberpunk application
document.addEventListener('DOMContentLoaded', () => {
    new CyberMajiSafeApp();
});

// Add mobile menu toggle functionality
document.addEventListener('DOMContentLoaded', () => {
    const mobileToggle = document.createElement('button');
    mobileToggle.className = 'mobile-menu-toggle';
    mobileToggle.innerHTML = '<i class="fas fa-bars"></i>';
    document.body.appendChild(mobileToggle);
    
    mobileToggle.addEventListener('click', () => {
        document.querySelector('.cyber-nav').classList.toggle('open');
    });
});

// Add CSS animations for notifications
const style = document.createElement('style');
style.textContent = `
    @keyframes slideOutRight {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
    
    .notification {
        display: flex;
        align-items: center;
        gap: 10px;
    }
    
    .notification i {
        font-size: 16px;
    }
`;
document.head.appendChild(style);

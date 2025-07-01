/**
 * Lakehouse Explorer Web Interface
 * JavaScript functionality for the web interface
 */

class LakehouseExplorer {
    constructor() {
        this.currentNamespace = null;
        this.currentTable = null;
        this.tables = [];
        this.namespaces = [];
        
        this.init();
    }

    init() {
        this.checkConnection();
        this.loadOverview();
        this.loadNamespaces();
        this.loadTables();
        this.setupEventListeners();
    }

    setupEventListeners() {
        // Search functionality
        const searchInput = document.getElementById('searchInput');
        if (searchInput) {
            let searchTimeout;
            searchInput.addEventListener('input', (e) => {
                clearTimeout(searchTimeout);
                searchTimeout = setTimeout(() => {
                    this.searchTables(e.target.value);
                }, 300);
            });
        }

        // Refresh button
        const refreshBtn = document.getElementById('refreshBtn');
        if (refreshBtn) {
            refreshBtn.addEventListener('click', () => {
                this.refreshData();
            });
        }

        // Preview limit change
        const previewLimit = document.getElementById('previewLimit');
        if (previewLimit) {
            previewLimit.addEventListener('change', () => {
                if (this.currentTable) {
                    this.loadTablePreview(this.currentTable.namespace, this.currentTable.name);
                }
            });
        }

        // SQL Query execution
        const executeQueryBtn = document.getElementById('executeQueryBtn');
        if (executeQueryBtn) {
            executeQueryBtn.addEventListener('click', () => {
                this.executeQuery();
            });
        }

        // Statistics loading
        const loadStatsBtn = document.getElementById('loadStatsBtn');
        if (loadStatsBtn) {
            loadStatsBtn.addEventListener('click', () => {
                if (this.currentTable) {
                    this.loadTableStatistics(this.currentTable.namespace, this.currentTable.name);
                }
                }
            });
        }

        // Refresh preview button
        const refreshPreview = document.getElementById('refreshPreview');
        if (refreshPreview) {
            refreshPreview.addEventListener('click', () => {
                if (this.currentTable) {
                    this.loadTablePreview(this.currentTable.namespace, this.currentTable.name);
                }
            });
        }
    }

    async checkConnection() {
        try {
            const response = await fetch('/api/status');
            const data = await response.json();
            
            const statusElement = document.getElementById('connectionStatus');
            if (data.connected) {
                statusElement.className = 'connection-status status-connected';
                statusElement.innerHTML = '<i class="fas fa-check-circle me-1"></i><span>Connected</span>';
            } else {
                statusElement.className = 'connection-status status-disconnected';
                statusElement.innerHTML = '<i class="fas fa-exclamation-circle me-1"></i><span>Disconnected</span>';
                this.showToast('Connection Error', data.message, 'error');
            }
        } catch (error) {
            console.error('Connection check failed:', error);
            const statusElement = document.getElementById('connectionStatus');
            statusElement.className = 'connection-status status-disconnected';
            statusElement.innerHTML = '<i class="fas fa-times-circle me-1"></i><span>Error</span>';
        }
    }

    async loadOverview() {
        try {
            const response = await fetch('/api/overview');
            const data = await response.json();
            
            if (data.status === 'success') {
                document.getElementById('totalNamespaces').textContent = data.overview.total_namespaces;
                document.getElementById('totalTables').textContent = data.overview.total_tables;
            }
        } catch (error) {
            console.error('Failed to load overview:', error);
        }
    }

    async loadNamespaces() {
        try {
            const response = await fetch('/api/namespaces');
            const data = await response.json();
            
            const namespaceList = document.getElementById('namespaceList');
            
            if (data.status === 'success') {
                this.namespaces = data.namespaces;
                
                if (data.namespaces.length === 0) {
                    namespaceList.innerHTML = '<p class="text-muted">No namespaces found</p>';
                    return;
                }

                let html = '';
                html += `<div class="namespace-item ${!this.currentNamespace ? 'active' : ''}" 
                             onclick="app.selectNamespace(null)">
                            <i class="fas fa-globe me-2"></i>
                            All Namespaces
                         </div>`;
                
                data.namespaces.forEach(namespace => {
                    const isActive = this.currentNamespace === namespace ? 'active' : '';
                    html += `<div class="namespace-item ${isActive}" 
                                 onclick="app.selectNamespace('${namespace}')">
                                <i class="fas fa-folder me-2"></i>
                                ${namespace}
                             </div>`;
                });
                
                namespaceList.innerHTML = html;
            } else {
                namespaceList.innerHTML = `<p class="text-danger">Error: ${data.message}</p>`;
            }
        } catch (error) {
            console.error('Failed to load namespaces:', error);
            document.getElementById('namespaceList').innerHTML = 
                '<p class="text-danger">Failed to load namespaces</p>';
        }
    }

    async loadTables(namespace = null) {
        try {
            let url = '/api/tables';
            if (namespace) {
                url += `?namespace=${encodeURIComponent(namespace)}`;
            }
            
            const response = await fetch(url);
            const data = await response.json();
            
            const tablesList = document.getElementById('tablesList');
            const tableListTitle = document.getElementById('tableListTitle');
            
            if (data.status === 'success') {
                this.tables = data.tables;
                
                // Update title
                if (namespace) {
                    tableListTitle.textContent = `Tables in ${namespace}`;
                } else {
                    tableListTitle.textContent = 'All Tables';
                }
                
                if (data.tables.length === 0) {
                    tablesList.innerHTML = '<p class="text-muted">No tables found</p>';
                    return;
                }

                this.renderTables(data.tables);
            } else {
                tablesList.innerHTML = `<p class="text-danger">Error: ${data.message}</p>`;
            }
        } catch (error) {
            console.error('Failed to load tables:', error);
            document.getElementById('tablesList').innerHTML = 
                '<p class="text-danger">Failed to load tables</p>';
        }
    }

    renderTables(tables) {
        const tablesList = document.getElementById('tablesList');
        
        if (tables.length === 0) {
            tablesList.innerHTML = '<p class="text-muted">No tables found</p>';
            return;
        }

        let html = '';
        tables.forEach(table => {
            html += `
                <div class="table-item" onclick="app.showTableDetails('${table.namespace}', '${table.name}')">
                    <div class="d-flex justify-content-between align-items-center">
                        <div>
                            <h6 class="mb-1">
                                <i class="fas fa-table me-2"></i>
                                ${table.name}
                            </h6>
                            <span class="namespace-badge">${table.namespace}</span>
                        </div>
                        <div>
                            <i class="fas fa-chevron-right text-muted"></i>
                        </div>
                    </div>
                </div>
            `;
        });
        
        tablesList.innerHTML = html;
    }

    selectNamespace(namespace) {
        this.currentNamespace = namespace;
        
        // Update active state in sidebar
        document.querySelectorAll('.namespace-item').forEach(item => {
            item.classList.remove('active');
        });
        
        // Find and activate the clicked namespace
        document.querySelectorAll('.namespace-item').forEach(item => {
            const text = item.textContent.trim();
            if ((namespace === null && text === 'All Namespaces') || text === namespace) {
                item.classList.add('active');
            }
        });
        
        // Load tables for selected namespace
        this.loadTables(namespace);
    }

    async searchTables(query) {
        if (!query.trim()) {
            this.loadTables(this.currentNamespace);
            return;
        }

        try {
            const response = await fetch(`/api/search?q=${encodeURIComponent(query)}`);
            const data = await response.json();
            
            const tableListTitle = document.getElementById('tableListTitle');
            
            if (data.status === 'success') {
                tableListTitle.textContent = `Search Results (${data.count} found)`;
                this.renderTables(data.results);
            } else {
                document.getElementById('tablesList').innerHTML = 
                    `<p class="text-danger">Search error: ${data.message}</p>`;
            }
        } catch (error) {
            console.error('Search failed:', error);
            document.getElementById('tablesList').innerHTML = 
                '<p class="text-danger">Search failed</p>';
        }
    }

    async showTableDetails(namespace, tableName) {
        this.currentTable = { namespace, name: tableName };
        
        // Update modal title
        document.getElementById('modalTableName').textContent = 
            `${namespace}.${tableName}`;
        
        // Reset tab content
        document.getElementById('tableInfo').innerHTML = this.getLoadingHTML();
        document.getElementById('tableSchema').innerHTML = this.getLoadingHTML();
        document.getElementById('tablePreview').innerHTML = this.getLoadingHTML();
        
        // Show modal
        const modal = new bootstrap.Modal(document.getElementById('tableModal'));
        modal.show();
        
        // Load data
        this.loadTableInfo(namespace, tableName);
    }

    async loadTableInfo(namespace, tableName) {
        try {
            const response = await fetch(`/api/table/info?namespace=${encodeURIComponent(namespace)}&table=${encodeURIComponent(tableName)}`);
            const data = await response.json();
            
            if (data.status === 'success') {
                this.renderTableInfo(data.table_info);
                this.renderTableSchema(data.table_info.columns);
                this.loadTablePreview(namespace, tableName);
            } else {
                document.getElementById('tableInfo').innerHTML = 
                    `<div class="alert alert-danger">Error: ${data.message}</div>`;
            }
        } catch (error) {
            console.error('Failed to load table info:', error);
            document.getElementById('tableInfo').innerHTML = 
                '<div class="alert alert-danger">Failed to load table information</div>';
        }
    }

    renderTableInfo(info) {
        const html = `
            <div class="row">
                <div class="col-md-6">
                    <table class="table table-bordered">
                        <tr>
                            <th>Namespace</th>
                            <td>${info.namespace.join('.') || 'default'}</td>
                        </tr>
                        <tr>
                            <th>Table Name</th>
                            <td>${info.name}</td>
                        </tr>
                        <tr>
                            <th>Location</th>
                            <td><small class="text-muted">${info.location}</small></td>
                        </tr>
                        <tr>
                            <th>Schema ID</th>
                            <td>${info.schema_id}</td>
                        </tr>
                        <tr>
                            <th>Snapshots</th>
                            <td>${info.snapshots_count}</td>
                        </tr>
                        <tr>
                            <th>Current Snapshot</th>
                            <td>${info.current_snapshot_id || 'None'}</td>
                        </tr>
                        <tr>
                            <th>Created</th>
                            <td>${info.created_at ? new Date(info.created_at).toLocaleString() : 'Unknown'}</td>
                        </tr>
                    </table>
                </div>
                <div class="col-md-6">
                    ${info.partition_spec && info.partition_spec !== '[]' ? `
                        <h6>Partition Specification</h6>
                        <pre class="bg-light p-2 rounded">${info.partition_spec}</pre>
                    ` : ''}
                    
                    ${Object.keys(info.properties || {}).length > 0 ? `
                        <h6>Properties</h6>
                        <table class="table table-sm">
                            ${Object.entries(info.properties).map(([key, value]) => 
                                `<tr><th>${key}</th><td>${value}</td></tr>`
                            ).join('')}
                        </table>
                    ` : ''}
                </div>
            </div>
        `;
        
        document.getElementById('tableInfo').innerHTML = html;
    }

    renderTableSchema(columns) {
        if (!columns || columns.length === 0) {
            document.getElementById('tableSchema').innerHTML = 
                '<p class="text-muted">No schema information available</p>';
            return;
        }

        const html = `
            <div class="table-responsive">
                <table class="table table-striped">
                    <thead>
                        <tr>
                            <th>Column Name</th>
                            <th>Data Type</th>
                            <th>Required</th>
                            <th>Description</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${columns.map(col => `
                            <tr>
                                <td><strong>${col.name}</strong></td>
                                <td><code>${col.type}</code></td>
                                <td>
                                    ${col.required ? 
                                        '<span class="badge bg-success">Required</span>' : 
                                        '<span class="badge bg-secondary">Optional</span>'
                                    }
                                </td>
                                <td>${col.doc || '<em class="text-muted">No description</em>'}</td>
                            </tr>
                        `).join('')}
                    </tbody>
                </table>
            </div>
        `;
        
        document.getElementById('tableSchema').innerHTML = html;
    }

    async loadTablePreview(namespace, tableName) {
        const limit = document.getElementById('previewLimit').value || 10;
        
        try {
            document.getElementById('tablePreview').innerHTML = this.getLoadingHTML();
            
            const response = await fetch(`/api/table/preview?namespace=${encodeURIComponent(namespace)}&table=${encodeURIComponent(tableName)}&limit=${limit}`);
            const data = await response.json();
            
            if (data.status === 'success') {
                this.renderTablePreview(data.data);
            } else {
                document.getElementById('tablePreview').innerHTML = 
                    `<div class="alert alert-danger">Error: ${data.message}</div>`;
            }
        } catch (error) {
            console.error('Failed to load table preview:', error);
            document.getElementById('tablePreview').innerHTML = 
                '<div class="alert alert-danger">Failed to load table preview</div>';
        }
    }

    renderTablePreview(data) {
        if (!data.rows || data.rows.length === 0) {
            document.getElementById('tablePreview').innerHTML = 
                '<div class="alert alert-info">No data available or table is empty</div>';
            return;
        }

        const html = `
            <div class="mb-3">
                <small class="text-muted">
                    Showing ${data.rows.length} rows × ${data.columns.length} columns
                </small>
            </div>
            <div class="table-preview-container">
                <table class="table table-striped table-hover">
                    <thead class="table-dark">
                        <tr>
                            ${data.columns.map(col => `<th>${col}</th>`).join('')}
                        </tr>
                    </thead>
                    <tbody>
                        ${data.rows.map(row => `
                            <tr>
                                ${row.map(cell => `<td>${this.formatCellValue(cell)}</td>`).join('')}
                            </tr>
                        `).join('')}
                    </tbody>
                </table>
            </div>
            <div class="mt-3">
                <h6>Data Types</h6>
                <div class="row">
                    ${Object.entries(data.dtypes).map(([col, dtype]) => `
                        <div class="col-md-4 mb-1">
                            <small><strong>${col}:</strong> <code>${dtype}</code></small>
                        </div>
                    `).join('')}
                </div>
            </div>
        `;
        
        document.getElementById('tablePreview').innerHTML = html;
    }

    formatCellValue(value) {
        if (value === null || value === undefined) {
            return '<em class="text-muted">null</em>';
        }
        if (typeof value === 'string' && value.length > 100) {
            return value.substring(0, 100) + '...';
        }
        return value;
    }

    refreshData() {
        const refreshBtn = document.getElementById('refreshBtn');
        const originalHTML = refreshBtn.innerHTML;
        
        refreshBtn.innerHTML = '<i class="fas fa-spin fa-spinner me-1"></i>Refreshing...';
        refreshBtn.disabled = true;
        
        Promise.all([
            this.loadOverview(),
            this.loadNamespaces(),
            this.loadTables(this.currentNamespace)
        ]).finally(() => {
            refreshBtn.innerHTML = originalHTML;
            refreshBtn.disabled = false;
            this.showToast('Success', 'Data refreshed successfully', 'success');
        });
    }

    async executeQuery() {
        const queryText = document.getElementById('sqlQuery').value;
        if (!queryText.trim()) {
            this.showError('Please enter a SQL query');
            return;
        }

        if (!this.currentTable) {
            this.showError('Please select a table first');
            return;
        }

        const queryBtn = document.getElementById('executeQueryBtn');
        const originalText = queryBtn.textContent;
        queryBtn.textContent = 'Executing...';
        queryBtn.disabled = true;

        try {
            const response = await fetch(`/api/table/${this.currentTable.namespace}/${this.currentTable.name}/query`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    query: queryText,
                    limit: document.getElementById('queryLimit')?.value || 100
                })
            });

            const data = await response.json();

            if (data.query_result.success) {
                this.renderQueryResults(data.query_result);
            } else {
                this.showError(`Query Error: ${data.query_result.error}`);
            }

        } catch (error) {
            this.showError(`Error executing query: ${error.message}`);
        } finally {
            queryBtn.textContent = originalText;
            queryBtn.disabled = false;
        }
    }

    renderQueryResults(queryResult) {
        const container = document.getElementById('queryResults');
        if (!container) return;

        const result = queryResult.result;
        
        let html = `
            <div class="query-result-header">
                <h4>Query Results</h4>
                <p class="query-info">
                    <strong>Rows:</strong> ${result.row_count} | 
                    <strong>Engine:</strong> ${result.engine || 'duckdb'}
                </p>
            </div>
        `;

        if (result.data && result.data.length > 0) {
            html += '<div class="table-container">';
            html += '<table class="data-table">';
            
            // Headers
            html += '<thead><tr>';
            result.columns.forEach(col => {
                html += `<th>${col}</th>`;
            });
            html += '</tr></thead>';
            
            // Data rows
            html += '<tbody>';
            result.data.forEach(row => {
                html += '<tr>';
                row.forEach(cell => {
                    const cellValue = cell === null ? '<em>null</em>' : String(cell);
                    html += `<td>${cellValue}</td>`;
                });
                html += '</tr>';
            });
            html += '</tbody>';
            
            html += '</table>';
            html += '</div>';
        } else {
            html += '<p class="no-data">No data returned</p>';
        }

        container.innerHTML = html;
    }

    async loadTableStatistics(namespace, tableName) {
        const statsBtn = document.getElementById('loadStatsBtn');
        const originalText = statsBtn.textContent;
        statsBtn.textContent = 'Loading...';
        statsBtn.disabled = true;

        try {
            const response = await fetch(`/api/table/${namespace}/${tableName}/statistics`);
            const data = await response.json();

            if (data.statistics) {
                this.renderTableStatistics(data.statistics);
            } else {
                this.showError('Failed to load statistics');
            }

        } catch (error) {
            this.showError(`Error loading statistics: ${error.message}`);
        } finally {
            statsBtn.textContent = originalText;
            statsBtn.disabled = false;
        }
    }

    renderTableStatistics(stats) {
        const container = document.getElementById('tableStatistics');
        if (!container) return;

        let html = `
            <div class="statistics-header">
                <h4>Table Statistics</h4>
                <p class="stats-engine">Engine: ${stats.engine || 'duckdb'}</p>
            </div>
            
            <div class="stats-summary">
                <div class="stat-item">
                    <label>Total Rows:</label>
                    <span>${stats.total_rows.toLocaleString()}</span>
                </div>
                <div class="stat-item">
                    <label>Distinct Rows:</label>
                    <span>${stats.distinct_rows.toLocaleString()}</span>
                </div>
            </div>
        `;

        if (stats.column_statistics) {
            html += '<div class="column-statistics">';
            html += '<h5>Column Statistics</h5>';
            html += '<div class="stats-table-container">';
            html += '<table class="stats-table">';
            html += '<thead><tr><th>Column</th><th>Count</th><th>Distinct</th><th>Nulls</th><th>Null %</th></tr></thead>';
            html += '<tbody>';

            Object.entries(stats.column_statistics).forEach(([col, colStats]) => {
                if (colStats.error) {
                    html += `<tr><td>${col}</td><td colspan="4">Error: ${colStats.error}</td></tr>`;
                } else {
                    html += `
                        <tr>
                            <td><strong>${col}</strong></td>
                            <td>${colStats.count.toLocaleString()}</td>
                            <td>${colStats.distinct_count.toLocaleString()}</td>
                            <td>${colStats.null_count.toLocaleString()}</td>
                            <td>${colStats.null_percentage}%</td>
                        </tr>
                    `;
                }
            });

            html += '</tbody></table>';
            html += '</div>';
            html += '</div>';
        }

        if (stats.note) {
            html += `<p class="stats-note"><em>${stats.note}</em></p>`;
        }

        container.innerHTML = html;
    }

    getLoadingHTML() {
        return `
            <div class="text-center">
                <div class="loading-spinner"></div>
                <p class="mt-2 text-muted">Loading...</p>
            </div>
        `;
    }

    showToast(title, message, type = 'info') {
        const toastContainer = document.querySelector('.toast-container');
        const toastId = 'toast-' + Date.now();
        
        const bgClass = {
            'success': 'bg-success',
            'error': 'bg-danger',
            'warning': 'bg-warning',
            'info': 'bg-info'
        }[type] || 'bg-info';
        
        const toastHTML = `
            <div id="${toastId}" class="toast ${bgClass} text-white" role="alert">
                <div class="toast-header">
                    <strong class="me-auto">${title}</strong>
                    <button type="button" class="btn-close btn-close-white" data-bs-dismiss="toast"></button>
                </div>
                <div class="toast-body">
                    ${message}
                </div>
            </div>
        `;
        
        toastContainer.insertAdjacentHTML('beforeend', toastHTML);
        
        const toastElement = document.getElementById(toastId);
        const toast = new bootstrap.Toast(toastElement, { delay: 5000 });
        toast.show();
        
        // Remove toast element after it's hidden
        toastElement.addEventListener('hidden.bs.toast', () => {
            toastElement.remove();
        });
    }

    showError(message) {
        const errorContainer = document.getElementById('errorContainer');
        if (errorContainer) {
            errorContainer.innerHTML = `
                <div class="alert alert-danger alert-dismissible fade show" role="alert">
                    <i class="fas fa-exclamation-circle me-2"></i>
                    ${message}
                    <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                </div>
            `;
        }
    }
}

// Initialize the application
const app = new LakehouseExplorer();

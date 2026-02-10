import { useState, useEffect } from 'react';
import axios from 'axios';
import { Bar, Pie } from 'react-chartjs-2';
import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    BarElement,
    Title,
    Tooltip,
    Legend,
    ArcElement
} from 'chart.js';
import {
    Activity,
    Upload,
    Wind,
    Thermometer,
    Gauge,
    Database,
    Sun,
    Moon,
    Beaker,
    TrendingUp,
    Download,
    LogOut,
    Clock,
    FileText,
    Calendar,
    ChevronRight,
    Menu,
    X
} from 'lucide-react';
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import {
    Card,
    CardContent,
    CardDescription,
    CardHeader,
    CardTitle
} from "@/components/ui/card";

// Register ChartJS components
ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend, ArcElement);

// Theme chart colors matching the cn theme
const chartColors = {
    bar: {
        background: 'rgba(114, 227, 173, 0.7)',
        border: '#72e3ad'
    },
    pie: [
        { bg: 'rgba(114, 227, 173, 0.7)', border: '#72e3ad' },   // mint green (primary)
        { bg: 'rgba(59, 130, 246, 0.7)', border: '#3b82f6' },    // blue
        { bg: 'rgba(139, 92, 246, 0.7)', border: '#8b5cf6' },    // purple
        { bg: 'rgba(245, 158, 11, 0.7)', border: '#f59e0b' },    // amber
        { bg: 'rgba(16, 185, 129, 0.7)', border: '#10b981' },    // emerald
        { bg: 'rgba(236, 72, 153, 0.7)', border: '#ec4899' },    // pink
        { bg: 'rgba(6, 182, 212, 0.7)', border: '#06b6d4' },     // cyan
        { bg: 'rgba(249, 115, 22, 0.7)', border: '#f97316' },    // orange
    ]
};

const API_BASE = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000';

const Dashboard = ({ authHeader, onLogout, darkMode, toggleDarkMode }) => {
    const [stats, setStats] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');
    const [batchId, setBatchId] = useState(null);
    const [recentUploads, setRecentUploads] = useState([]);
    const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

    // Fetch recent uploads on mount
    useEffect(() => {
        fetchHistory();
    }, [authHeader]);

    const fetchHistory = async () => {
        if (!authHeader) return;
        try {
            const response = await axios.get(`${API_BASE}/api/upload/`, {
                headers: { 'Authorization': authHeader }
            });
            setRecentUploads(response.data);
        } catch (err) {
            console.error("Failed to fetch history", err);
        }
    };

    const handleBatchSelect = async (id) => {
        setLoading(true);
        setError('');
        try {
            const response = await axios.get(`${API_BASE}/api/batch/${id}/`, {
                headers: { 'Authorization': authHeader }
            });
            setStats(response.data.statistics);
            setBatchId(response.data.batch_id);
            // Scroll to stats
            window.scrollTo({ top: 400, behavior: 'smooth' });
        } catch (err) {
            setError('Failed to load report.');
            if (err.response?.status === 401) onLogout();
        } finally {
            setLoading(false);
        }
    };

    const handleFileUpload = async (event) => {
        const file = event.target.files[0];
        if (!file) return;

        const formData = new FormData();
        formData.append('file', file);

        setLoading(true);
        setError('');

        try {
            const response = await axios.post(`${API_BASE}/api/upload/`, formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                    'Authorization': authHeader
                },
            });
            setStats(response.data.statistics);
            setBatchId(response.data.batch_id);
            fetchHistory(); // Refresh history
        } catch (err) {
            if (err.response?.status === 401) {
                setError('Session expired. Please login again.');
                onLogout();
            } else {
                setError('Failed to upload file. Make sure Server is running!');
            }
            console.error(err);
        } finally {
            setLoading(false);
        }
    };

    const formatDate = (dateString) => {
        return new Date(dateString).toLocaleDateString('en-US', {
            month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit'
        });
    };

    const [isRecentUploadsOpen, setIsRecentUploadsOpen] = useState(true);

    return (
        <div className="min-h-screen bg-background text-foreground transition-colors duration-300 flex flex-col">
            {/* Navbar - Mobile Responsive */}
            <nav className="sticky top-0 z-50 border-b border-border bg-background/80 backdrop-blur-md">
                <div className="container mx-auto flex h-14 sm:h-16 items-center justify-between px-3 sm:px-4">
                    <div className="flex items-center gap-2 sm:gap-3 min-w-0">
                        <div className="flex h-8 w-8 sm:h-10 sm:w-10 items-center justify-center rounded-lg bg-primary/10 text-primary-foreground overflow-hidden flex-shrink-0">
                            <img src="/image.png" alt="Logo" className="h-6 w-6 sm:h-8 sm:w-8 object-contain" />
                        </div>
                        <h1 className="text-sm sm:text-lg font-bold tracking-tight truncate">
                            <span className="hidden sm:inline">Chemical Equipment Parameter Visualizer</span>
                            <span className="sm:hidden">Parameter Visualizer</span>
                        </h1>
                    </div>

                    {/* Desktop Nav Buttons */}
                    <div className="hidden sm:flex items-center gap-3">
                        <Button
                            onClick={() => batchId && window.open(`${API_BASE}/api/export-pdf/${batchId}/`, '_blank')}
                            size="sm"
                            disabled={!batchId}
                            className="bg-primary hover:bg-primary/90 text-primary-foreground"
                        >
                            <Download className="h-4 w-4 mr-2" />
                            Export PDF
                        </Button>
                        <Button
                            variant="outline"
                            size="icon"
                            onClick={toggleDarkMode}
                            className="rounded-full"
                        >
                            {darkMode ? <Sun className="h-4 w-4" /> : <Moon className="h-4 w-4" />}
                        </Button>
                        <Button
                            variant="ghost"
                            size="icon"
                            onClick={onLogout}
                            className="text-muted-foreground hover:text-foreground rounded-full"
                        >
                            <LogOut className="h-4 w-4" />
                        </Button>
                    </div>

                    {/* Mobile Menu Button */}
                    <div className="flex sm:hidden items-center gap-2">
                        <Button
                            variant="outline"
                            size="icon"
                            onClick={toggleDarkMode}
                            className="rounded-full h-8 w-8"
                        >
                            {darkMode ? <Sun className="h-4 w-4" /> : <Moon className="h-4 w-4" />}
                        </Button>
                        <Button
                            variant="ghost"
                            size="icon"
                            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
                            className="h-8 w-8"
                        >
                            {mobileMenuOpen ? <X className="h-5 w-5" /> : <Menu className="h-5 w-5" />}
                        </Button>
                    </div>
                </div>

                {/* Mobile Menu Dropdown */}
                {mobileMenuOpen && (
                    <div className="sm:hidden border-t border-border bg-background p-3 space-y-2 animate-in slide-in-from-top-2">
                        <Button
                            onClick={() => {
                                batchId && window.open(`${API_BASE}/api/export-pdf/${batchId}/`, '_blank');
                                setMobileMenuOpen(false);
                            }}
                            size="sm"
                            disabled={!batchId}
                            className="w-full bg-primary hover:bg-primary/90 text-primary-foreground"
                        >
                            <Download className="h-4 w-4 mr-2" />
                            Export PDF
                        </Button>
                        <Button
                            variant="outline"
                            size="sm"
                            onClick={() => {
                                onLogout();
                                setMobileMenuOpen(false);
                            }}
                            className="w-full"
                        >
                            <LogOut className="h-4 w-4 mr-2" />
                            Logout
                        </Button>
                    </div>
                )}
            </nav>

            <main className="container mx-auto py-4 sm:py-8 px-3 sm:px-4 space-y-4 sm:space-y-6 flex-1">
                {/* Hero + Upload Section - Stacked on mobile, side-by-side on desktop */}
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-4 sm:gap-6">
                    {/* Left: Hero Content */}
                    <div className="relative overflow-hidden rounded-xl sm:rounded-2xl bg-card p-5 sm:p-8 border border-border shadow-lg flex flex-col justify-between">
                        <div className="absolute top-0 right-0 w-48 sm:w-64 h-48 sm:h-64 bg-primary/20 rounded-full blur-3xl -translate-y-1/2 translate-x-1/2 animate-pulse" />
                        <div className="absolute bottom-0 left-0 w-36 sm:w-48 h-36 sm:h-48 bg-secondary/20 rounded-full blur-3xl translate-y-1/2 -translate-x-1/2 animate-pulse" style={{ animationDelay: '1s' }} />

                        <div className="relative z-10 space-y-3 sm:space-y-4">
                            <h2 className="text-xl sm:text-3xl font-bold tracking-tight text-foreground">
                                Chemical Equipment Parameter Visualizer
                            </h2>
                            <p className="text-sm sm:text-base text-muted-foreground leading-relaxed">
                                Upload a CSV file to generate summary analytics including total equipment count, average operating values, and equipment type distribution.
                            </p>
                        </div>

                        {/* Last Uploaded Button */}
                        {recentUploads.length > 0 && (
                            <button
                                onClick={() => handleBatchSelect(recentUploads[0].id)}
                                className="relative z-10 mt-4 sm:mt-6 flex items-center justify-between p-3 sm:p-4 bg-background/50 backdrop-blur-sm rounded-lg sm:rounded-xl border border-border/50 hover:border-primary/50 transition-all group"
                            >
                                <div className="flex items-center gap-2 sm:gap-3 min-w-0">
                                    <Database className="h-4 w-4 sm:h-5 sm:w-5 text-muted-foreground flex-shrink-0" />
                                    <span className="text-xs sm:text-sm text-foreground truncate">Last uploaded: {recentUploads[0].filename}</span>
                                </div>
                                <ChevronRight className="h-4 w-4 text-muted-foreground group-hover:translate-x-1 transition-transform flex-shrink-0" />
                            </button>
                        )}
                    </div>

                    {/* Right: Upload Section */}
                    <Card className="border border-border bg-card shadow-lg">
                        <CardContent className="p-5 sm:p-8 flex flex-col items-center justify-center text-center space-y-3 sm:space-y-4">
                            <div className="flex h-12 w-12 sm:h-16 sm:w-16 items-center justify-center rounded-full bg-primary/10">
                                <Upload className="h-6 w-6 sm:h-8 sm:w-8 text-primary" />
                            </div>
                            <div>
                                <CardTitle className="text-lg sm:text-xl mb-1 sm:mb-2">Upload Equipment Data</CardTitle>
                                <CardDescription className="text-sm sm:text-base">
                                    Upload CSV to analyze summary statistics
                                </CardDescription>
                            </div>

                            <Label
                                htmlFor="csv_file"
                                className="inline-flex items-center gap-2 px-4 sm:px-6 py-2.5 sm:py-3 bg-primary hover:bg-primary/90 text-primary-foreground rounded-lg cursor-pointer transition-colors font-medium text-sm sm:text-base"
                            >
                                <Upload className="h-4 w-4" />
                                Browse File
                            </Label>
                            <Input
                                id="csv_file"
                                type="file"
                                accept=".csv"
                                onChange={handleFileUpload}
                                disabled={loading}
                                className="hidden"
                            />

                            {recentUploads.length > 0 && (
                                <p className="text-xs sm:text-sm text-muted-foreground truncate max-w-full">
                                    Last uploaded: {recentUploads[0].filename}
                                </p>
                            )}

                            {loading && (
                                <div className="flex items-center justify-center gap-2 p-3 sm:p-4 bg-primary/5 rounded-lg w-full">
                                    <div className="h-4 w-4 border-2 border-primary border-t-transparent rounded-full animate-spin" />
                                    <span className="text-xs sm:text-sm text-primary font-medium">Processing your data...</span>
                                </div>
                            )}

                            {error && (
                                <div className="p-3 sm:p-4 text-xs sm:text-sm text-destructive bg-destructive/10 rounded-lg border border-destructive/20 flex items-center gap-2 w-full">
                                    <Activity className="h-4 w-4 flex-shrink-0" />
                                    <span className="truncate">{error}</span>
                                </div>
                            )}
                        </CardContent>
                    </Card>
                </div>

                {/* Stats Overview - 2 columns on mobile, 4 on desktop */}
                {stats && (
                    <div className="space-y-4 sm:space-y-6 animate-in fade-in-50 slide-in-from-bottom-5 duration-500">
                        <div className="grid gap-3 sm:gap-4 grid-cols-2 lg:grid-cols-4">
                            <Card className="group hover-lift border-primary/20">
                                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-1 sm:pb-2 p-3 sm:p-6">
                                    <CardTitle className="text-xs sm:text-sm font-medium text-primary">Total Equipment</CardTitle>
                                    <div className="h-7 w-7 sm:h-9 sm:w-9 rounded-full bg-primary/10 flex items-center justify-center group-hover:scale-110 transition-transform duration-300">
                                        <Database className="h-4 w-4 sm:h-5 sm:w-5 text-primary" />
                                    </div>
                                </CardHeader>
                                <CardContent className="p-3 sm:p-6 pt-0">
                                    <div className="text-2xl sm:text-3xl font-bold tracking-tight">{stats.total_count}</div>
                                    <p className="text-[10px] sm:text-xs text-muted-foreground mt-1 font-medium">Units registered</p>
                                </CardContent>
                            </Card>

                            <Card className="group hover-lift border-blue-500/20">
                                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-1 sm:pb-2 p-3 sm:p-6">
                                    <CardTitle className="text-xs sm:text-sm font-medium text-blue-500">Avg Flowrate</CardTitle>
                                    <div className="h-7 w-7 sm:h-9 sm:w-9 rounded-full bg-blue-500/10 flex items-center justify-center group-hover:scale-110 transition-transform duration-300">
                                        <Wind className="h-4 w-4 sm:h-5 sm:w-5 text-blue-500" />
                                    </div>
                                </CardHeader>
                                <CardContent className="p-3 sm:p-6 pt-0">
                                    <div className="text-2xl sm:text-3xl font-bold tracking-tight">{stats.average_flowrate}</div>
                                    <p className="text-[10px] sm:text-xs text-muted-foreground mt-1 font-medium">m³/hr avg flow</p>
                                </CardContent>
                            </Card>

                            <Card className="group hover-lift border-purple-500/20">
                                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-1 sm:pb-2 p-3 sm:p-6">
                                    <CardTitle className="text-xs sm:text-sm font-medium text-purple-500">Avg Pressure</CardTitle>
                                    <div className="h-7 w-7 sm:h-9 sm:w-9 rounded-full bg-purple-500/10 flex items-center justify-center group-hover:scale-110 transition-transform duration-300">
                                        <Gauge className="h-4 w-4 sm:h-5 sm:w-5 text-purple-500" />
                                    </div>
                                </CardHeader>
                                <CardContent className="p-3 sm:p-6 pt-0">
                                    <div className="text-2xl sm:text-3xl font-bold tracking-tight">{stats.average_pressure}</div>
                                    <p className="text-[10px] sm:text-xs text-muted-foreground mt-1 font-medium">Pa avg pressure</p>
                                </CardContent>
                            </Card>

                            <Card className="group hover-lift border-amber-500/20">
                                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-1 sm:pb-2 p-3 sm:p-6">
                                    <CardTitle className="text-xs sm:text-sm font-medium text-amber-500">Avg Temperature</CardTitle>
                                    <div className="h-7 w-7 sm:h-9 sm:w-9 rounded-full bg-amber-500/10 flex items-center justify-center group-hover:scale-110 transition-transform duration-300">
                                        <Thermometer className="h-4 w-4 sm:h-5 sm:w-5 text-amber-500" />
                                    </div>
                                </CardHeader>
                                <CardContent className="p-3 sm:p-6 pt-0">
                                    <div className="text-2xl sm:text-3xl font-bold tracking-tight">{stats.average_temperature}</div>
                                    <p className="text-[10px] sm:text-xs text-muted-foreground mt-1 font-medium">°C avg temp</p>
                                </CardContent>
                            </Card>
                        </div>

                        {/* Charts Section - Stacked on mobile, side by side on desktop */}
                        <div className="grid gap-4 sm:gap-6 grid-cols-1 lg:grid-cols-2">
                            <Card>
                                <CardHeader className="p-4 sm:p-6">
                                    <CardTitle className="flex items-center gap-2 text-base sm:text-lg">
                                        <img src="/bar-graph.png" alt="Distribution" className="h-5 w-5 sm:h-6 sm:w-6 object-contain" />
                                        Equipment Count by Type
                                    </CardTitle>
                                </CardHeader>
                                <CardContent className="p-4 sm:p-6 pt-0">
                                    <div className="h-[250px] sm:h-[320px] w-full">
                                        <Bar
                                            data={{
                                                labels: Object.keys(stats.type_distribution),
                                                datasets: [{
                                                    label: 'Count',
                                                    data: Object.values(stats.type_distribution),
                                                    backgroundColor: chartColors.bar.background,
                                                    borderColor: chartColors.bar.border,
                                                    borderWidth: 2,
                                                    borderRadius: 6,
                                                }]
                                            }}
                                            options={{
                                                responsive: true,
                                                maintainAspectRatio: false,
                                                plugins: {
                                                    legend: {
                                                        display: false,
                                                    }
                                                },
                                                scales: {
                                                    y: {
                                                        beginAtZero: true,
                                                        grid: {
                                                            color: 'rgba(131, 148, 150, 0.1)',
                                                        },
                                                        ticks: {
                                                            color: '#839496',
                                                            font: { size: 10 }
                                                        }
                                                    },
                                                    x: {
                                                        grid: {
                                                            display: false,
                                                        },
                                                        ticks: {
                                                            color: '#839496',
                                                            font: { size: 10 },
                                                            maxRotation: 45,
                                                            minRotation: 0
                                                        }
                                                    }
                                                }
                                            }}
                                        />
                                    </div>
                                </CardContent>
                            </Card>

                            <Card>
                                <CardHeader className="p-4 sm:p-6">
                                    <CardTitle className="flex items-center gap-2 text-base sm:text-lg">
                                        <img src="/pie-chart.png" alt="Share" className="h-5 w-5 sm:h-6 sm:w-6 object-contain" />
                                        Equipment Type Share
                                    </CardTitle>
                                </CardHeader>
                                <CardContent className="p-4 sm:p-6 pt-0">
                                    <div className="h-[250px] sm:h-[320px] flex items-center justify-center">
                                        <Pie
                                            data={{
                                                labels: Object.keys(stats.type_distribution),
                                                datasets: [{
                                                    label: 'Count',
                                                    data: Object.values(stats.type_distribution),
                                                    backgroundColor: chartColors.pie.map(c => c.bg),
                                                    borderColor: chartColors.pie.map(c => c.border),
                                                    borderWidth: 2,
                                                }],
                                            }}
                                            options={{
                                                responsive: true,
                                                maintainAspectRatio: false,
                                                plugins: {
                                                    legend: {
                                                        position: window.innerWidth < 640 ? 'bottom' : 'right',
                                                        labels: {
                                                            boxWidth: 10,
                                                            padding: 12,
                                                            color: '#839496',
                                                            font: { size: 11 }
                                                        }
                                                    }
                                                }
                                            }}
                                        />
                                    </div>
                                </CardContent>
                            </Card>
                        </div>
                    </div>
                )}

                {/* Recent Uploads - Collapsible Section at Bottom */}
                <Card className="border-border bg-card/50 backdrop-blur-sm">
                    <CardHeader
                        className="cursor-pointer flex flex-row items-center justify-between py-3 sm:py-4 px-4 sm:px-6"
                        onClick={() => setIsRecentUploadsOpen(!isRecentUploadsOpen)}
                    >
                        <CardTitle className="text-sm sm:text-base flex items-center gap-2">
                            <FileText className="h-4 w-4 sm:h-5 sm:w-5 text-muted-foreground" />
                            Recent Uploads
                            <span className="text-muted-foreground font-normal text-xs sm:text-sm">(Last 5)</span>
                        </CardTitle>
                        <ChevronRight className={`h-4 w-4 sm:h-5 sm:w-5 text-muted-foreground transition-transform duration-200 ${isRecentUploadsOpen ? 'rotate-90' : ''}`} />
                    </CardHeader>
                    {isRecentUploadsOpen && (
                        <CardContent className="pt-0 px-4 sm:px-6 pb-4">
                            {recentUploads.length === 0 ? (
                                <div className="py-4 text-center text-muted-foreground text-xs sm:text-sm">
                                    No uploads yet. Upload a file to get started.
                                </div>
                            ) : (
                                <div className="divide-y divide-border/50">
                                    {recentUploads.map((batch) => (
                                        <button
                                            key={batch.id}
                                            onClick={() => handleBatchSelect(batch.id)}
                                            className={`w-full text-left py-2.5 sm:py-3 px-2 transition-all hover:bg-muted/50 group flex items-center justify-between gap-2 ${batchId === batch.id ? 'bg-primary/5' : ''}`}
                                        >
                                            <div className="flex items-center gap-2 sm:gap-3 min-w-0">
                                                <FileText className="h-4 w-4 text-muted-foreground flex-shrink-0" />
                                                <span className="font-medium text-xs sm:text-sm text-foreground group-hover:text-primary transition-colors truncate">
                                                    {batch.filename}
                                                </span>
                                            </div>
                                            <div className="flex items-center gap-2 sm:gap-4 text-xs sm:text-sm text-muted-foreground flex-shrink-0">
                                                <span className="hidden xs:inline">{formatDate(batch.uploaded_at)}</span>
                                                <Clock className="h-3 w-3 sm:h-4 sm:w-4" />
                                            </div>
                                        </button>
                                    ))}
                                </div>
                            )}
                        </CardContent>
                    )}
                </Card>
            </main>

            {/* Footer */}
            <footer className="text-center py-4 sm:py-6 text-xs sm:text-sm text-muted-foreground border-t border-border bg-background/50 backdrop-blur-sm px-4">
                <p>Chemical Equipment Parameter Visualizer • Built with React & Shadcn UI</p>
            </footer>
        </div>
    );
};

export default Dashboard;

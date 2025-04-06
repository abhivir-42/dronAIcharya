import React, { useState, useEffect } from 'react';
import { 
  Container, 
  Grid, 
  Card, 
  CardContent, 
  Typography, 
  Button, 
  Box,
  LinearProgress,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  Divider,
  Chip,
  ButtonGroup,
  CircularProgress
} from '@mui/material';
import { 
  BarChart, 
  PieChart, 
  TrendingUp, 
  Group, 
  School, 
  Translate, 
  VideoLibrary,
  QuestionAnswer,
  RefreshRounded,
  CloudDownload,
  Warning
} from '@mui/icons-material';

// This would be replaced with actual API clients
const api = {
  fetchClassData: async (classId) => {
    // Simulate API call
    return new Promise((resolve) => {
      setTimeout(() => {
        resolve({
          className: '7B Mathematics',
          date: new Date().toLocaleDateString(),
          topics: ['Algebraic Expressions', 'Linear Equations'],
          progress: 65,
          students: {
            engaged: 18,
            struggling: 7,
            idle: 3
          }
        });
      }, 500);
    });
  },
  
  fetchLearningGaps: async (classId) => {
    // Simulate API call
    return new Promise((resolve) => {
      setTimeout(() => {
        resolve([
          {
            id: 'gap1',
            description: 'Coefficient multiplication',
            affectedStudents: 8,
            severity: 'high'
          },
          {
            id: 'gap2',
            description: 'Variable basics',
            affectedStudents: 5,
            severity: 'medium'
          }
        ]);
      }, 700);
    });
  }
};

// Component for displaying class engagement
const ClassEngagement = ({ data, loading }) => {
  if (loading) return <CircularProgress />;
  
  return (
    <Card variant="outlined" sx={{ height: '100%' }}>
      <CardContent>
        <Typography variant="h6" gutterBottom>
          Real-Time Class Engagement
        </Typography>
        
        <Box sx={{ 
          height: 200, 
          bgcolor: 'action.hover', 
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          mb: 2
        }}>
          <Typography variant="body2">
            [Heatmap Visualization Would Appear Here]
          </Typography>
        </Box>
        
        <Grid container spacing={2}>
          <Grid item xs={4}>
            <Chip 
              label={`Engaged: ${data.students.engaged}`} 
              color="success" 
              variant="outlined"
              sx={{ width: '100%' }}
            />
          </Grid>
          <Grid item xs={4}>
            <Chip 
              label={`Struggling: ${data.students.struggling}`} 
              color="warning" 
              variant="outlined"
              sx={{ width: '100%' }}
            />
          </Grid>
          <Grid item xs={4}>
            <Chip 
              label={`Idle: ${data.students.idle}`} 
              color="error" 
              variant="outlined"
              sx={{ width: '100%' }}
            />
          </Grid>
        </Grid>
      </CardContent>
    </Card>
  );
};

// Component for displaying learning gaps
const LearningGaps = ({ gaps, loading }) => {
  if (loading) return <CircularProgress />;
  
  return (
    <Card variant="outlined" sx={{ height: '100%' }}>
      <CardContent>
        <Typography variant="h6" gutterBottom>
          Learning Gaps Detected
        </Typography>
        
        <List dense>
          {gaps.map(gap => (
            <ListItem key={gap.id}>
              <ListItemIcon>
                {gap.severity === 'high' ? 
                  <Warning color="error" /> : 
                  <Warning color="warning" />
                }
              </ListItemIcon>
              <ListItemText 
                primary={`${gap.affectedStudents} students struggling with ${gap.description}`}
              />
            </ListItem>
          ))}
        </List>
      </CardContent>
    </Card>
  );
};

// Component for recommended actions
const RecommendedActions = ({ gaps, loading }) => {
  if (loading) return <CircularProgress />;
  
  // Actions would be determined by AI based on learning gaps
  const actions = [
    { label: 'Generate Simplified Examples', icon: <QuestionAnswer /> },
    { label: 'Create Visual Explanation', icon: <VideoLibrary /> },
    { label: 'Form Peer Learning Groups', icon: <Group /> },
    { label: 'Adapt Current Lesson', icon: <RefreshRounded /> },
    { label: 'Translate to Hindi/Marathi', icon: <Translate /> }
  ];
  
  return (
    <Card variant="outlined" sx={{ height: '100%' }}>
      <CardContent>
        <Typography variant="h6" gutterBottom>
          Recommended Actions
        </Typography>
        
        <List dense>
          {actions.map((action, index) => (
            <ListItem key={index}>
              <Button 
                variant="outlined" 
                startIcon={action.icon}
                fullWidth
                sx={{ justifyContent: 'flex-start', textTransform: 'none' }}
              >
                {action.label}
              </Button>
            </ListItem>
          ))}
        </List>
      </CardContent>
    </Card>
  );
};

// Main Dashboard Component
const TeacherDashboard = () => {
  const [classData, setClassData] = useState(null);
  const [learningGaps, setLearningGaps] = useState([]);
  const [loading, setLoading] = useState(true);
  const [offlineMode, setOfflineMode] = useState(false);
  
  useEffect(() => {
    const loadData = async () => {
      try {
        const classInfo = await api.fetchClassData('class-7b');
        const gaps = await api.fetchLearningGaps('class-7b');
        
        setClassData(classInfo);
        setLearningGaps(gaps);
        setLoading(false);
      } catch (error) {
        console.error("Failed to load data:", error);
        // Enable offline mode with cached data if available
        setOfflineMode(true);
        setLoading(false);
        
        // In a real app, would attempt to load from local storage/IndexedDB
      }
    };
    
    loadData();
  }, []);
  
  return (
    <Container maxWidth="lg" sx={{ mt: 3, mb: 4 }}>
      {offlineMode && (
        <Box sx={{ mb: 2, p: 1, bgcolor: 'warning.light', borderRadius: 1 }}>
          <Typography variant="body2">
            <b>Working in offline mode</b> - Using cached data. Some features may be limited.
          </Typography>
        </Box>
      )}
      
      <Card sx={{ mb: 3 }}>
        <CardContent>
          <Grid container alignItems="center" justifyContent="space-between">
            <Grid item>
              <Typography variant="h5">
                {loading ? 'Loading...' : `Class Overview: ${classData?.className}`}
              </Typography>
            </Grid>
            <Grid item>
              <Typography variant="body1">
                Date: {loading ? '...' : classData?.date}
              </Typography>
            </Grid>
          </Grid>
        </CardContent>
      </Card>
      
      <Grid container spacing={3}>
        {/* Left panel */}
        <Grid item xs={12} md={4}>
          <Card variant="outlined" sx={{ mb: 3 }}>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Today's Topics
              </Typography>
              
              {loading ? (
                <CircularProgress size={20} />
              ) : (
                <List dense>
                  {classData?.topics.map((topic, index) => (
                    <ListItem key={index}>
                      <ListItemText primary={topic} />
                    </ListItem>
                  ))}
                </List>
              )}
              
              <Divider sx={{ my: 1 }} />
              
              <Typography variant="body2" gutterBottom>
                Learning Progress:
              </Typography>
              
              {loading ? (
                <CircularProgress size={20} />
              ) : (
                <>
                  <LinearProgress 
                    variant="determinate" 
                    value={classData?.progress || 0} 
                    sx={{ height: 10, borderRadius: 5 }}
                  />
                  <Typography variant="body2" sx={{ mt: 1 }}>
                    {classData?.progress}% Complete
                  </Typography>
                </>
              )}
            </CardContent>
          </Card>
          
          <LearningGaps gaps={learningGaps} loading={loading} />
        </Grid>
        
        {/* Right panel */}
        <Grid item xs={12} md={8}>
          <Grid container spacing={3}>
            <Grid item xs={12}>
              <ClassEngagement data={classData || {students: {engaged: 0, struggling: 0, idle: 0}}} loading={loading} />
            </Grid>
            
            <Grid item xs={12}>
              <RecommendedActions gaps={learningGaps} loading={loading} />
            </Grid>
          </Grid>
        </Grid>
      </Grid>
      
      {/* Quick tools */}
      <Card sx={{ mt: 3 }}>
        <CardContent>
          <Typography variant="body1" gutterBottom>
            Quick Tools:
          </Typography>
          
          <ButtonGroup variant="outlined" aria-label="quick tools">
            <Button startIcon={<Group />}>Take Attendance</Button>
            <Button startIcon={<QuestionAnswer />}>Quiz Generator</Button>
            <Button startIcon={<School />}>Share Screen</Button>
            <Button 
              startIcon={<CloudDownload />}
              onClick={() => alert('Content saved for offline use')}
            >
              Save Offline
            </Button>
          </ButtonGroup>
        </CardContent>
      </Card>
    </Container>
  );
};

export default TeacherDashboard; 
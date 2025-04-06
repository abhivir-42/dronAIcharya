# DronAIcharya System Data Flow

This diagram illustrates how data flows between the different components of the DronAIcharya system, showing the interactions between services and how information is processed.

```mermaid
flowchart TB
    subgraph Users
        T[Teacher]
        S[Student]
        P[Parent]
    end
    
    subgraph Frontend["Frontend Layer"]
        TD[Teacher Dashboard]
        SV[Student View]
        PD[Parent Dashboard]
        CM[Content Management]
    end
    
    subgraph API["API Gateway Layer"]
        AG[API Gateway & Auth]
    end
    
    subgraph Services["Core Services"]
        ALS[Adaptive Learning Service]
        CG[Content Generation Service]
        CA[Classroom Analytics Service]
        TP[Teacher Professional Support]
        NF[Notification Service]
    end
    
    subgraph Storage["Data & Storage"]
        DB[(Database)]
        FS[File Storage]
        LC[Local Cache]
    end
    
    subgraph AI["AI & ML Layer"]
        ML[ML Models]
        NLP[NLP Processing]
        CV[Computer Vision]
        MG[Manim Generator]
    end
    
    %% User interactions
    T -->|Interacts with| TD
    S -->|Interacts with| SV
    P -->|Interacts with| PD
    T -->|Creates content| CM
    
    %% Frontend to API
    TD -->|Requests data| AG
    SV -->|Submits answers| AG
    PD -->|Checks progress| AG
    CM -->|Submits content| AG
    
    %% API to Services
    AG -->|Routes requests| ALS
    AG -->|Routes requests| CG
    AG -->|Routes requests| CA
    AG -->|Routes requests| TP
    AG -->|Routes requests| NF
    
    %% Services to AI
    ALS -->|Requests adaptation| ML
    ALS -->|Analyzes text| NLP
    CG -->|Generates visuals| MG
    CA -->|Processes video| CV
    CA -->|Analyzes patterns| ML
    
    %% Services to Storage
    ALS -->|Stores/retrieves data| DB
    CG -->|Stores content| FS
    CA -->|Logs analytics| DB
    TP -->|Stores resources| FS
    NF -->|Reads user prefs| DB
    
    %% Local storage
    SV -.->|Caches for offline| LC
    TD -.->|Caches for offline| LC
    FS -.->|Syncs when online| LC
    
    %% Service Interactions
    ALS <-->|Shares learning gaps| CA
    CG <-->|Creates content for| ALS
    NF <---->|Triggers based on| CA
    TP <---->|Guided by| CA
    
    %% Styling
    classDef users fill:#f9f,stroke:#333,stroke-width:1px
    classDef frontend fill:#bbf,stroke:#333,stroke-width:1px
    classDef api fill:#bfb,stroke:#333,stroke-width:1px
    classDef services fill:#fbb,stroke:#333,stroke-width:1px
    classDef storage fill:#fbf,stroke:#333,stroke-width:1px
    classDef ai fill:#bff,stroke:#333,stroke-width:1px
    
    class Users users
    class Frontend frontend
    class API api
    class Services services
    class Storage storage
    class AI ai
```

## Real-time Event Processing Flow

This diagram shows how the system handles real-time classroom events and generates adaptive responses.

```mermaid
sequenceDiagram
    participant T as Teacher
    participant TD as Teacher Dashboard
    participant CA as Classroom Analytics
    participant ALS as Adaptive Learning
    participant CG as Content Generator
    participant S as Students
    
    T->>TD: Start lesson monitoring
    TD->>CA: Initialize classroom tracking
    
    loop Every 5 minutes
        CA->>S: Capture engagement metrics
        S-->>CA: Behavior & interaction data
        CA->>CA: Process & analyze patterns
        CA->>TD: Update real-time metrics
        
        alt Engagement dropping
            CA->>ALS: Alert about engagement issue
            ALS->>ALS: Generate adaptation plan
            ALS->>TD: Suggest teaching adaptations
            TD->>T: Show adaptation recommendations
            T->>TD: Select recommendation
            TD->>CG: Request engaging content
            CG->>TD: Deliver adapted content
            TD->>S: Present new content
        else Learning gaps detected
            CA->>ALS: Inform of specific gaps
            ALS->>ALS: Identify remedial approaches
            ALS->>CG: Request targeted content
            CG->>TD: Deliver personalized exercises
            TD->>T: Show differentiated activities
            T->>S: Assign targeted exercises
        end
    end
    
    T->>TD: End lesson
    TD->>CA: Generate session summary
    CA->>ALS: Update learning profiles
    ALS->>ALS: Adjust future lesson plans
    TD->>T: Present lesson insights & recommendations
``` 
/**
 * Central Data Configuration File for the Hackathon Project
 * Member 1 (ML Team) can easily update dataset statistics and results here.
 */

export const datasetInfo = {
  // Flag indicating if actual ML dataset numbers have been inserted
  isUpdatedByML: false,
  statusMessage: "Pending ML Team (Member 1) Final Dataset Confirmation",
  name: "Face Mask Detection Dataset",
  source: "Kaggle / Custom Masked Face Dataset",
  classesCount: 2,
  classes: ["Mask (With Mask)", "No Mask (Without Mask)"],
  totalImages: "Pending ML Team",
  maskImages: "Pending ML Team",
  noMaskImages: "Pending ML Team",
  trainingImages: "Pending ML Team",
  validationImages: "Pending ML Team",
  imageDimensions: "224 x 224 x 3",
};

export const modelInfo = {
  architecture: "MobileNetV2",
  approach: "Transfer Learning (Pre-trained on ImageNet)",
  inputShape: "(224, 224, 3)",
  baseModelStatus: "Frozen Base Layers + Custom Dense Head",
  outputClasses: 2,
  activation: "Softmax / Sigmoid",
  rationale: "MobileNetV2 uses depthwise separable convolutions, making it ultra-lightweight, fast, and optimized for real-time web & mobile edge inference during live hackathon demos.",
  pipelineSteps: [
    {
      step: 1,
      title: "Input Frame / Image",
      desc: "Captures 2D RGB image frame from browser webcam or file upload.",
      icon: "Camera",
    },
    {
      step: 2,
      title: "Preprocessing",
      desc: "Resizes image to 224x224, converts color channels, and normalizes pixel values.",
      icon: "Cpu",
    },
    {
      step: 3,
      title: "MobileNetV2 Feature Extraction",
      desc: "Passes normalized array through pre-trained inverted residual blocks to extract rich spatial features.",
      icon: "Layers",
    },
    {
      step: 4,
      title: "Classification Head",
      desc: "Custom dense FC layer & dropout layers map extracted feature vectors to binary class logits.",
      icon: "GitFork",
    },
    {
      step: 5,
      title: "Prediction Output",
      desc: "Computes final classification label (Mask / No Mask) with confidence probability score.",
      icon: "CheckCircle2",
    },
  ],
};

export const resultsInfo = {
  // Flag indicating if actual ML training results have been inserted
  isUpdatedByML: false,
  statusMessage: "Awaiting final model training metrics and evaluation plots from Member 1 (ML Team).",
  metrics: {
    trainingAccuracy: { label: "Training Accuracy", value: "Pending ML", placeholder: "-- %" },
    validationAccuracy: { label: "Validation Accuracy", value: "Pending ML", placeholder: "-- %" },
    trainingLoss: { label: "Training Loss", value: "Pending ML", placeholder: "--" },
    validationLoss: { label: "Validation Loss", value: "Pending ML", placeholder: "--" },
  },
  assets: {
    accuracyGraph: null, // Replace with import or path e.g. "/src/assets/results/accuracy_plot.png"
    lossGraph: null,     // Replace with path e.g. "/src/assets/results/loss_plot.png"
    confusionMatrix: null, // Replace with path e.g. "/src/assets/results/confusion_matrix.png"
  },
};

export const technologiesData = [
  {
    category: "Frontend",
    items: [
      { name: "React", desc: "UI Library for component-based web architecture", color: "#61dafb" },
      { name: "JavaScript", desc: "ES6+ for interactive logic and state management", color: "#f7df1e" },
      { name: "HTML5", desc: "Semantic web page structure", color: "#e34f26" },
      { name: "CSS3", desc: "Modern styling, glassmorphism & responsive layouts", color: "#1572b6" },
    ],
  },
  {
    category: "AI / Machine Learning",
    items: [
      { name: "Python", desc: "Primary programming language for deep learning", color: "#3776ab" },
      { name: "TensorFlow", desc: "Open-source end-to-end machine learning platform", color: "#ff6f00" },
      { name: "Keras", desc: "High-level neural networks API", color: "#d00000" },
      { name: "MobileNetV2", desc: "Pre-trained deep CNN optimized for mobile/edge vision", color: "#00b4d8" },
    ],
  },
  {
    category: "Computer Vision & Backend",
    items: [
      { name: "OpenCV", desc: "Image processing, scaling and color format conversion", color: "#5c3ee8" },
      { name: "FastAPI", desc: "High-performance Python web framework for prediction API", color: "#059669" },
    ],
  },
  {
    category: "Development & Workflow",
    items: [
      { name: "Google Colab", desc: "Cloud GPU environment for ML model training", color: "#f9ab00" },
      { name: "GitHub", desc: "Version control and team collaboration", color: "#ffffff" },
    ],
  },
];

export const teamData = [
  {
    role: "Member 1: Machine Learning",
    name: "ML Specialist (Member 1)",
    responsibilities: [
      "Dataset curation & augmentation",
      "MobileNetV2 transfer learning setup",
      "Model training & hyperparameter tuning",
      "Accuracy & loss evaluation",
      "Model export (.h5 / SavedModel)",
    ],
    tag: "ML & AI",
  },
  {
    role: "Member 2: Frontend Development",
    name: "Frontend Engineer (Member 2)",
    responsibilities: [
      "React single-page application structure",
      "Responsive & interactive UI/UX design",
      "HTML5 MediaDevices browser webcam integration",
      "API service layer & state management",
      "Backend integration & status handling",
    ],
    tag: "UI / UX & React",
  },
  {
    role: "Member 3: Backend & Computer Vision",
    name: "Backend Developer (Member 3)",
    responsibilities: [
      "Python FastAPI server architecture",
      "GET /health and POST /predict REST endpoints",
      "OpenCV frame decoding & preprocessing pipeline",
      "TensorFlow model inference execution",
      "JSON response payload formatting",
    ],
    tag: "Backend & CV",
  },
];

-- ============================================================
-- Intel Briefing Plugin - Supabase Schema
-- Version: 1.0.0
-- Tables: 8 (rok_ naming convention)
-- ============================================================

-- Documents: Ingested content metadata and summaries
CREATE TABLE rok_intel_documents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    source_type TEXT NOT NULL CHECK (source_type IN ('youtube', 'url', 'pdf', 'markdown', 'text', 'article')),
    source_path TEXT,
    source_url TEXT,
    title TEXT NOT NULL,
    author TEXT,
    publish_date DATE,
    ingest_date TIMESTAMPTZ DEFAULT NOW(),
    content_hash TEXT UNIQUE,
    raw_summary TEXT,
    word_count INTEGER,
    trust_tier TEXT DEFAULT 'STANDARD' CHECK (trust_tier IN ('HIGH', 'MEDIUM', 'STANDARD')),
    classification TEXT CHECK (classification IN ('news', 'analysis', 'opinion', 'report', 'tutorial', 'discussion')),
    topics TEXT[],
    tags TEXT[],
    processed BOOLEAN DEFAULT FALSE,
    metadata JSONB DEFAULT '{}'::jsonb
);

CREATE INDEX idx_intel_documents_source_type ON rok_intel_documents(source_type);
CREATE INDEX idx_intel_documents_ingest_date ON rok_intel_documents(ingest_date DESC);
CREATE INDEX idx_intel_documents_topics ON rok_intel_documents USING GIN(topics);
CREATE INDEX idx_intel_documents_hash ON rok_intel_documents(content_hash);

-- Claims: Structured factual assertions extracted from documents
CREATE TABLE rok_intel_claims (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    document_id UUID REFERENCES rok_intel_documents(id) ON DELETE CASCADE,
    claim_text TEXT NOT NULL,
    category TEXT NOT NULL CHECK (category IN (
        'financial', 'geopolitical', 'technology', 'economic',
        'market', 'policy', 'military', 'social', 'energy', 'other'
    )),
    subcategory TEXT,
    claim_type TEXT NOT NULL CHECK (claim_type IN (
        'fact', 'prediction', 'analysis', 'opinion', 'recommendation'
    )),
    confidence_score DECIMAL(3,2) CHECK (confidence_score BETWEEN 0 AND 1),
    validation_status TEXT DEFAULT 'unvalidated' CHECK (validation_status IN (
        'unvalidated', 'confirmed', 'partially_confirmed', 'contradicted', 'contested'
    )),
    validation_sources JSONB DEFAULT '[]'::jsonb,
    extraction_date TIMESTAMPTZ DEFAULT NOW(),
    expires_at DATE,
    superseded_by UUID REFERENCES rok_intel_claims(id),
    tags TEXT[],
    metadata JSONB DEFAULT '{}'::jsonb
);

CREATE INDEX idx_intel_claims_category ON rok_intel_claims(category);
CREATE INDEX idx_intel_claims_document ON rok_intel_claims(document_id);
CREATE INDEX idx_intel_claims_validation ON rok_intel_claims(validation_status);
CREATE INDEX idx_intel_claims_type ON rok_intel_claims(claim_type);
CREATE INDEX idx_intel_claims_tags ON rok_intel_claims USING GIN(tags);
CREATE INDEX idx_intel_claims_extraction ON rok_intel_claims(extraction_date DESC);

-- Predictions: Trackable forecasts with outcomes
CREATE TABLE rok_intel_predictions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    claim_id UUID REFERENCES rok_intel_claims(id),
    document_id UUID REFERENCES rok_intel_documents(id),
    prediction_text TEXT NOT NULL,
    category TEXT NOT NULL CHECK (category IN ('financial', 'geopolitical', 'technology', 'economic', 'other')),
    subcategory TEXT,
    timeframe TEXT,
    target_date DATE,
    initial_confidence DECIMAL(3,2) CHECK (initial_confidence BETWEEN 0 AND 1),
    current_confidence DECIMAL(3,2) CHECK (current_confidence BETWEEN 0 AND 1),
    outcome TEXT DEFAULT 'pending' CHECK (outcome IN ('pending', 'correct', 'partially_correct', 'incorrect', 'indeterminate')),
    outcome_notes TEXT,
    outcome_date DATE,
    source_author TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    tags TEXT[],
    metadata JSONB DEFAULT '{}'::jsonb
);

CREATE INDEX idx_intel_predictions_category ON rok_intel_predictions(category);
CREATE INDEX idx_intel_predictions_outcome ON rok_intel_predictions(outcome);
CREATE INDEX idx_intel_predictions_target ON rok_intel_predictions(target_date);
CREATE INDEX idx_intel_predictions_tags ON rok_intel_predictions USING GIN(tags);

-- Master Briefings: Versioned cumulative synthesis snapshots
CREATE TABLE rok_intel_briefings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    version INTEGER NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    document_count INTEGER,
    claim_count INTEGER,
    prediction_count INTEGER,
    executive_summary TEXT,
    key_developments TEXT,
    financial_section TEXT,
    geopolitical_section TEXT,
    technology_section TEXT,
    consensus_themes JSONB,
    contested_topics JSONB,
    confidence_summary JSONB,
    full_briefing_md TEXT,
    trigger_document_id UUID REFERENCES rok_intel_documents(id),
    metadata JSONB DEFAULT '{}'::jsonb
);

CREATE INDEX idx_intel_briefings_version ON rok_intel_briefings(version DESC);
CREATE INDEX idx_intel_briefings_created ON rok_intel_briefings(created_at DESC);

-- Prediction Accuracy: Historical tracking and Brier scores
CREATE TABLE rok_intel_prediction_accuracy (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    evaluation_date DATE NOT NULL,
    category TEXT,
    total_evaluated INTEGER,
    correct_count INTEGER,
    partially_correct_count INTEGER,
    incorrect_count INTEGER,
    accuracy_rate DECIMAL(5,2),
    brier_score DECIMAL(5,4),
    metadata JSONB DEFAULT '{}'::jsonb
);

CREATE INDEX idx_intel_accuracy_date ON rok_intel_prediction_accuracy(evaluation_date DESC);
CREATE INDEX idx_intel_accuracy_category ON rok_intel_prediction_accuracy(category);

-- Source Trust Registry: Track source reliability over time
CREATE TABLE rok_intel_sources (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    source_name TEXT UNIQUE NOT NULL,
    source_type TEXT CHECK (source_type IN ('youtube_channel', 'publication', 'analyst', 'institution', 'other')),
    trust_tier TEXT DEFAULT 'STANDARD' CHECK (trust_tier IN ('HIGH', 'MEDIUM', 'STANDARD', 'LOW')),
    domain_expertise TEXT[],
    prediction_accuracy DECIMAL(5,2),
    documents_analyzed INTEGER DEFAULT 0,
    last_analyzed TIMESTAMPTZ,
    notes TEXT,
    metadata JSONB DEFAULT '{}'::jsonb
);

CREATE INDEX idx_intel_sources_trust ON rok_intel_sources(trust_tier);
CREATE INDEX idx_intel_sources_name ON rok_intel_sources(source_name);
CREATE INDEX idx_intel_sources_expertise ON rok_intel_sources USING GIN(domain_expertise);

-- Alerts: Topic watch alerts for claim matching
CREATE TABLE rok_intel_alerts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    topic TEXT NOT NULL,
    category TEXT,
    keywords TEXT[],
    active BOOLEAN DEFAULT TRUE,
    match_count INTEGER DEFAULT 0,
    last_matched TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    metadata JSONB DEFAULT '{}'::jsonb
);

CREATE INDEX idx_intel_alerts_active ON rok_intel_alerts(active);
CREATE INDEX idx_intel_alerts_topic ON rok_intel_alerts(topic);

-- Theses: Evolving narrative tracking with confidence history
CREATE TABLE rok_intel_theses (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    thesis_text TEXT NOT NULL,
    category TEXT CHECK (category IN ('financial', 'geopolitical', 'technology', 'economic', 'other')),
    initial_confidence DECIMAL(3,2) CHECK (initial_confidence BETWEEN 0 AND 1),
    current_confidence DECIMAL(3,2) CHECK (current_confidence BETWEEN 0 AND 1),
    confidence_history JSONB DEFAULT '[]'::jsonb,
    linked_claim_ids UUID[] DEFAULT '{}',
    status TEXT DEFAULT 'active' CHECK (status IN ('active', 'confirmed', 'invalidated', 'archived')),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    tags TEXT[],
    metadata JSONB DEFAULT '{}'::jsonb
);

CREATE INDEX idx_intel_theses_status ON rok_intel_theses(status);
CREATE INDEX idx_intel_theses_category ON rok_intel_theses(category);

-- Enable RLS on all tables
ALTER TABLE rok_intel_documents ENABLE ROW LEVEL SECURITY;
ALTER TABLE rok_intel_claims ENABLE ROW LEVEL SECURITY;
ALTER TABLE rok_intel_predictions ENABLE ROW LEVEL SECURITY;
ALTER TABLE rok_intel_briefings ENABLE ROW LEVEL SECURITY;
ALTER TABLE rok_intel_prediction_accuracy ENABLE ROW LEVEL SECURITY;
ALTER TABLE rok_intel_sources ENABLE ROW LEVEL SECURITY;
ALTER TABLE rok_intel_alerts ENABLE ROW LEVEL SECURITY;
ALTER TABLE rok_intel_theses ENABLE ROW LEVEL SECURITY;

-- Service role full access policies
CREATE POLICY "Service role full access" ON rok_intel_documents FOR ALL USING (true) WITH CHECK (true);
CREATE POLICY "Service role full access" ON rok_intel_claims FOR ALL USING (true) WITH CHECK (true);
CREATE POLICY "Service role full access" ON rok_intel_predictions FOR ALL USING (true) WITH CHECK (true);
CREATE POLICY "Service role full access" ON rok_intel_briefings FOR ALL USING (true) WITH CHECK (true);
CREATE POLICY "Service role full access" ON rok_intel_prediction_accuracy FOR ALL USING (true) WITH CHECK (true);
CREATE POLICY "Service role full access" ON rok_intel_sources FOR ALL USING (true) WITH CHECK (true);
CREATE POLICY "Service role full access" ON rok_intel_alerts FOR ALL USING (true) WITH CHECK (true);
CREATE POLICY "Service role full access" ON rok_intel_theses FOR ALL USING (true) WITH CHECK (true);

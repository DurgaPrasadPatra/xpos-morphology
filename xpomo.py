import streamlit as st
import json
from datetime import datetime

# Configure page
st.set_page_config(
    page_title="Complete UD Morphological Decision Support",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Complete UD morphological data
@st.cache_data
def load_complete_morphology_data():
    return {
        'NOUN_analysis': {
            'title': 'NOUN Complete Analysis (NN, NNP, NNS)',
            'description': 'Comprehensive noun selection with all morphological features',
            'upos': 'NOUN',
            'xpos_tags': ['NN', 'NNP', 'NNS'],
            'scenarios': [
                {
                    'context': 'Number and Case Selection',
                    'question': 'Which noun form should I use?',
                    'recommendations': [
                        {
                            'choice': 'Use NN (Singular Nominative)',
                            'xpos': 'NN',
                            'feats': 'Number=Sing | Case=Nom | Gender=Masc/Fem/Neut',
                            'when': 'For singular subjects',
                            'examples': [
                                'The cat sleeps (cat=NN, Number=Sing, Case=Nom)',
                                'A student reads (student=NN, Number=Sing, Case=Nom)',
                                'This house stands (house=NN, Number=Sing, Case=Nom)'
                            ],
                            'morphological_rules': 'NN: Number=Sing | Case=Nom | Gender=M/F/N',
                            'decision_factors': ['Subject position', 'Singular verb', 'No object marking']
                        },
                        {
                            'choice': 'Use NNS (Plural Nominative)',
                            'xpos': 'NNS',
                            'feats': 'Number=Plur | Case=Acc',
                            'when': 'For plural objects',
                            'examples': [
                                'I see cats (cats=NNS, Number=Plur, Case=Acc)',
                                'She reads books (books=NNS, Number=Plur, Case=Acc)',
                                'They built houses (houses=NNS, Number=Plur, Case=Acc)'
                            ],
                            'morphological_rules': 'NNS: Number=Plur | Case=Acc',
                            'decision_factors': ['Object position', 'Plural form', 'Accusative case']
                        },
                        {
                            'choice': 'Use NNP (Proper Noun)',
                            'xpos': 'NNP',
                            'feats': 'Number=Sing | Case=Nom',
                            'when': 'For names and proper nouns',
                            'examples': [
                                'John works here (John=NNP, Number=Sing, Case=Nom)',
                                'Paris is beautiful (Paris=NNP, Number=Sing, Case=Nom)',
                                'Microsoft announced (Microsoft=NNP, Number=Sing, Case=Nom)'
                            ],
                            'morphological_rules': 'NNP: Number=Sing | Case=Nom',
                            'decision_factors': ['Proper name', 'Capitalized', 'Unique reference']
                        }
                    ]
                }
            ]
        },
        'VERB_analysis': {
            'title': 'VERB Complete Analysis (VM, VINF, VAUX)',
            'description': 'Comprehensive verb selection with tense, mood, honorificity',
            'upos': 'VERB',
            'xpos_tags': ['VM', 'VINF', 'VAUX'],
            'scenarios': [
                {
                    'context': 'Finite Verb Forms',
                    'question': 'Which finite verb form should I use?',
                    'recommendations': [
                        {
                            'choice': 'Use VM (Present Finite)',
                            'xpos': 'VM',
                            'feats': 'VerbForm=Fin | Tense=Pres/Past/Fut | Person=1/2/3',
                            'when': 'For main verbs showing tense and person',
                            'examples': [
                                'I walk daily (walk=VM, VerbForm=Fin, Tense=Pres, Person=1)',
                                'She walks fast (walks=VM, VerbForm=Fin, Tense=Pres, Person=3)',
                                'They walked yesterday (walked=VM, VerbForm=Fin, Tense=Past)'
                            ],
                            'morphological_rules': 'VM: VerbForm=Fin | Tense=Pres/Past/Fut | Person=1/2/3',
                            'decision_factors': ['Main verb', 'Shows tense', 'Person agreement']
                        },
                        {
                            'choice': 'Use VINF (Infinitive)',
                            'xpos': 'VINF',
                            'feats': 'VerbForm=Inf',
                            'when': 'For infinitive forms',
                            'examples': [
                                'I want to walk (walk=VINF, VerbForm=Inf)',
                                'She can walk (walk=VINF, VerbForm=Inf)',
                                'They need to go (go=VINF, VerbForm=Inf)'
                            ],
                            'morphological_rules': 'VINF: VerbForm=Inf',
                            'decision_factors': ['After modals', 'To + verb', 'No tense marking']
                        },
                        {
                            'choice': 'Use VAUX (Auxiliary)',
                            'xpos': 'VAUX',
                            'feats': 'Mood=Ind | VerbForm=Part',
                            'when': 'For auxiliary verbs',
                            'examples': [
                                'He has walked (has=VAUX, Mood=Ind)',
                                'She is walking (is=VAUX, VerbForm=Part)',
                                'They were seen (were=VAUX, VerbForm=Part)'
                            ],
                            'morphological_rules': 'VAUX: Mood=Ind | VerbForm=Part',
                            'decision_factors': ['Helper verb', 'Compound tense', 'Passive construction']
                        }
                    ]
                },
                {
                    'context': 'Honorificity in Verbs',
                    'question': 'Should I use honorific verb forms?',
                    'recommendations': [
                        {
                            'choice': 'Use VM (Honorific)',
                            'xpos': 'VM',
                            'feats': 'VerbForm=Fin | Honorificity=Yes',
                            'when': 'When showing respect to subject/addressee',
                            'examples': [
                                'The professor teaches (teaches=VM, Honorificity=Yes)',
                                'Please come, sir (come=VM, Honorificity=Yes)',
                                'May I help you? (help=VM, Honorificity=Yes)'
                            ],
                            'morphological_rules': 'VM: VerbForm=Fin | Honorificity=Yes',
                            'decision_factors': ['Respectful context', 'Formal situation', 'Superior status']
                        },
                        {
                            'choice': 'Use VM (Non-Honorific)',
                            'xpos': 'VM',
                            'feats': 'VerbForm=Fin | Honorificity=No',
                            'when': 'For casual or equal-status contexts',
                            'examples': [
                                'My friend walks (walks=VM, Honorificity=No)',
                                'Kids play outside (play=VM, Honorificity=No)',
                                'We eat lunch (eat=VM, Honorificity=No)'
                            ],
                            'morphological_rules': 'VM: VerbForm=Fin | Honorificity=No',
                            'decision_factors': ['Casual context', 'Equal status', 'Informal setting']
                        }
                    ]
                }
            ]
        },
        'ADVERB_analysis': {
            'title': 'ADVERB Complete Analysis (RB)',
            'description': 'Complete adverb selection with semantic types and degrees',
            'upos': 'ADV',
            'xpos_tags': ['RB'],
            'scenarios': [
                {
                    'context': 'Adverb Semantic Types',
                    'question': 'Which semantic type of adverb?',
                    'recommendations': [
                        {
                            'choice': 'Use RB (Manner)',
                            'xpos': 'RB',
                            'feats': 'Degree=Pos | AdvType=Manner',
                            'when': 'For describing how actions are performed',
                            'examples': [
                                'She walks quickly (quickly=RB, AdvType=Manner)',
                                'He speaks softly (softly=RB, AdvType=Manner)',
                                'They work carefully (carefully=RB, AdvType=Manner)'
                            ],
                            'morphological_rules': 'RB: Degree=Pos | AdvType=Manner',
                            'decision_factors': ['How question', 'Action modification', 'Process description']
                        },
                        {
                            'choice': 'Use RB (Temporal)',
                            'xpos': 'RB',
                            'feats': 'Degree=Pos | AdvType=Temporal',
                            'when': 'For indicating when actions occur',
                            'examples': [
                                'She arrived yesterday (yesterday=RB, AdvType=Temporal)',
                                'He always comes early (always=RB, AdvType=Temporal)',
                                'They will leave soon (soon=RB, AdvType=Temporal)'
                            ],
                            'morphological_rules': 'RB: Degree=Pos | AdvType=Temporal',
                            'decision_factors': ['When question', 'Time reference', 'Temporal sequence']
                        },
                        {
                            'choice': 'Use RB (Locative)',
                            'xpos': 'RB',
                            'feats': 'Degree=Pos | AdvType=Locative',
                            'when': 'For indicating where actions occur',
                            'examples': [
                                'She works here (here=RB, AdvType=Locative)',
                                'He lives nearby (nearby=RB, AdvType=Locative)',
                                'They went upstairs (upstairs=RB, AdvType=Locative)'
                            ],
                            'morphological_rules': 'RB: Degree=Pos | AdvType=Locative',
                            'decision_factors': ['Where question', 'Location reference', 'Spatial relation']
                        },
                        {
                            'choice': 'Use RB (Frequentative)',
                            'xpos': 'RB',
                            'feats': 'Degree=Pos | AdvType=Frequentative',
                            'when': 'For indicating how often actions occur',
                            'examples': [
                                'She often visits (often=RB, AdvType=Frequentative)',
                                'He rarely complains (rarely=RB, AdvType=Frequentative)',
                                'They always help (always=RB, AdvType=Frequentative)'
                            ],
                            'morphological_rules': 'RB: Degree=Pos | AdvType=Frequentative',
                            'decision_factors': ['How often', 'Frequency indication', 'Habitual pattern']
                        },
                        {
                            'choice': 'Use RB (Resultative)',
                            'xpos': 'RB',
                            'feats': 'Degree=Pos | AdvType=Resultative',
                            'when': 'For indicating results or outcomes',
                            'examples': [
                                'Door opened completely (completely=RB, AdvType=Resultative)',
                                'She finished successfully (successfully=RB, AdvType=Resultative)',
                                'They solved it perfectly (perfectly=RB, AdvType=Resultative)'
                            ],
                            'morphological_rules': 'RB: Degree=Pos | AdvType=Resultative',
                            'decision_factors': ['End state', 'Completion degree', 'Result emphasis']
                        }
                    ]
                }
            ]
        },
        'PRONOUN_analysis': {
            'title': 'PRONOUN Complete Analysis (PRP, V_PRON-HON)',
            'description': 'Complete pronoun selection with honorificity and case',
            'upos': 'PRON',
            'xpos_tags': ['PRP', 'V_PRON-HON'],
            'scenarios': [
                {
                    'context': 'Person and Case Selection',
                    'question': 'Which pronoun form should I use?',
                    'recommendations': [
                        {
                            'choice': 'Use PRP (1st Person Nom)',
                            'xpos': 'PRP',
                            'feats': 'Person=1 | Number=Sing | Case=Nom | Honorificity=No',
                            'when': 'For first person subjects',
                            'examples': [
                                'I am walking (I=PRP, Person=1, Case=Nom)',
                                'I can help (I=PRP, Person=1, Case=Nom)',
                                'I understand (I=PRP, Person=1, Case=Nom)'
                            ],
                            'morphological_rules': 'PRP: Person=1 | Number=Sing | Case=Nom',
                            'decision_factors': ['Speaker reference', 'Subject position', 'First person']
                        },
                        {
                            'choice': 'Use PRP (2nd Person Acc)',
                            'xpos': 'PRP',
                            'feats': 'Person=2 | Number=Sing | Case=Acc | Honorificity=No',
                            'when': 'For second person objects',
                            'examples': [
                                'I help you (you=PRP, Person=2, Case=Acc)',
                                'She called you (you=PRP, Person=2, Case=Acc)',
                                'They invited you (you=PRP, Person=2, Case=Acc)'
                            ],
                            'morphological_rules': 'PRP: Person=2 | Number=Sing | Case=Acc',
                            'decision_factors': ['Addressee reference', 'Object position', 'Casual context']
                        }
                    ]
                },
                {
                    'context': 'Honorificity in Pronouns',
                    'question': 'Should I use honorific pronouns?',
                    'recommendations': [
                        {
                            'choice': 'Use V_PRON-HON (Honorific)',
                            'xpos': 'V_PRON-HON',
                            'feats': 'Person=2/3 | Case=Nom/Acc | Honorificity=Yes',
                            'when': 'When showing respect to addressee/referent',
                            'examples': [
                                'You are kind, sir (You=V_PRON-HON, Honorificity=Yes)',
                                'May I help you? (you=V_PRON-HON, Honorificity=Yes)',
                                'His Excellency arrived (His=V_PRON-HON, Honorificity=Yes)'
                            ],
                            'morphological_rules': 'V_PRON-HON: Person=2/3 | Honorificity=Yes',
                            'decision_factors': ['Respectful address', 'Formal context', 'High status person']
                        },
                        {
                            'choice': 'Use PRP (Non-Honorific)',
                            'xpos': 'PRP',
                            'feats': 'Person=1/2/3 | Case=Nom/Acc | Honorificity=No',
                            'when': 'For casual or equal-status contexts',
                            'examples': [
                                'You can sit here (you=PRP, Honorificity=No)',
                                'He is my friend (he=PRP, Honorificity=No)',
                                'They are students (they=PRP, Honorificity=No)'
                            ],
                            'morphological_rules': 'PRP: Person=1/2/3 | Honorificity=No',
                            'decision_factors': ['Equal status', 'Informal context', 'Casual relationship']
                        }
                    ]
                }
            ]
        },
        'CONJUNCTION_analysis': {
            'title': 'CONJUNCTION Complete Analysis (CC, SC)',
            'description': 'Complete conjunction selection with coordination types',
            'upos': 'CCONJ/SCONJ',
            'xpos_tags': ['CC', 'SC'],
            'scenarios': [
                {
                    'context': 'Coordination Types',
                    'question': 'Which coordination type should I use?',
                    'recommendations': [
                        {
                            'choice': 'Use CC (Coordinating)',
                            'xpos': 'CC',
                            'feats': 'ConjType=Coordinating',
                            'when': 'For connecting equal elements',
                            'examples': [
                                'John and Mary (and=CC, ConjType=Coordinating)',
                                'Run or walk (or=CC, ConjType=Coordinating)',
                                'Smart but lazy (but=CC, ConjType=Coordinating)'
                            ],
                            'morphological_rules': 'CC: ConjType=Coordinating',
                            'decision_factors': ['Equal elements', 'Same level', 'Addition/contrast']
                        },
                        {
                            'choice': 'Use CC (Correlative)',
                            'xpos': 'CC',
                            'feats': 'ConjType=Correlative',
                            'when': 'For paired conjunctions',
                            'examples': [
                                'Both John and Mary (both...and=CC, ConjType=Correlative)',
                                'Either run or walk (either...or=CC, ConjType=Correlative)',
                                'Neither smart nor lazy (neither...nor=CC, ConjType=Correlative)'
                            ],
                            'morphological_rules': 'CC: ConjType=Correlative',
                            'decision_factors': ['Paired conjunctions', 'Emphasis', 'Binary choice']
                        },
                        {
                            'choice': 'Use SC (Subordinating)',
                            'xpos': 'SC',
                            'feats': 'ConjType=Subordinating',
                            'when': 'For dependent clauses',
                            'examples': [
                                'Because he was tired (because=SC, ConjType=Subordinating)',
                                'When she arrives (when=SC, ConjType=Subordinating)',
                                'If you want (if=SC, ConjType=Subordinating)'
                            ],
                            'morphological_rules': 'SC: ConjType=Subordinating',
                            'decision_factors': ['Dependent clause', 'Subordination', 'Hierarchy']
                        }
                    ]
                }
            ]
        },
        'DETERMINER_analysis': {
            'title': 'DETERMINER Complete Analysis (DT)',
            'description': 'Complete determiner selection with definiteness and deixis',
            'upos': 'DET',
            'xpos_tags': ['DT'],
            'scenarios': [
                {
                    'context': 'Article vs Demonstrative',
                    'question': 'Should I use article or demonstrative?',
                    'recommendations': [
                        {
                            'choice': 'Use DT (Article)',
                            'xpos': 'DT',
                            'feats': 'PronType=Art',
                            'when': 'For definite/indefinite articles',
                            'examples': [
                                'The book is here (the=DT, PronType=Art)',
                                'A cat is sleeping (a=DT, PronType=Art)',
                                'An apple fell (an=DT, PronType=Art)'
                            ],
                            'morphological_rules': 'DT: PronType=Art',
                            'decision_factors': ['General reference', 'Definiteness', 'First/repeated mention']
                        },
                        {
                            'choice': 'Use DT (Demonstrative)',
                            'xpos': 'DT',
                            'feats': 'PronType=Dem',
                            'when': 'For pointing to specific items',
                            'examples': [
                                'This book is mine (this=DT, PronType=Dem)',
                                'That car is fast (that=DT, PronType=Dem)',
                                'These ideas are good (these=DT, PronType=Dem)'
                            ],
                            'morphological_rules': 'DT: PronType=Dem',
                            'decision_factors': ['Specific pointing', 'Distance indication', 'Contextual reference']
                        }
                    ]
                }
            ]
        },
        'PREPOSITION_analysis': {
            'title': 'PREPOSITION Complete Analysis (IN)',
            'description': 'Complete preposition selection with case government',
            'upos': 'ADP',
            'xpos_tags': ['IN'],
            'scenarios': [
                {
                    'context': 'Case Government',
                    'question': 'Which case should this preposition govern?',
                    'recommendations': [
                        {
                            'choice': 'Use IN (Locative)',
                            'xpos': 'IN',
                            'feats': 'Case=Loc',
                            'when': 'For location and time',
                            'examples': [
                                'In the house (in=IN, Case=Loc)',
                                'At the store (at=IN, Case=Loc)',
                                'On the table (on=IN, Case=Loc)'
                            ],
                            'morphological_rules': 'IN: Case=Loc',
                            'decision_factors': ['Static location', 'Time periods', 'Containment']
                        },
                        {
                            'choice': 'Use IN (Instrumental)',
                            'xpos': 'IN',
                            'feats': 'Case=Ins',
                            'when': 'For instrument or means',
                            'examples': [
                                'With a hammer (with=IN, Case=Ins)',
                                'By train (by=IN, Case=Ins)',
                                'Through hard work (through=IN, Case=Ins)'
                            ],
                            'morphological_rules': 'IN: Case=Ins',
                            'decision_factors': ['Instrument', 'Means', 'Method']
                        }
                    ]
                }
            ]
        },
        'NUMBER_analysis': {
            'title': 'NUMBER Complete Analysis (CD)',
            'description': 'Complete number selection with cardinal/ordinal types',
            'upos': 'NUM',
            'xpos_tags': ['CD'],
            'scenarios': [
                {
                    'context': 'Number Type Selection',
                    'question': 'Should I use cardinal or ordinal?',
                    'recommendations': [
                        {
                            'choice': 'Use CD (Cardinal)',
                            'xpos': 'CD',
                            'feats': 'NumType=Card',
                            'when': 'For counting or quantity',
                            'examples': [
                                'Three books (three=CD, NumType=Card)',
                                'Five cats (five=CD, NumType=Card)',
                                'Ten dollars (ten=CD, NumType=Card)'
                            ],
                            'morphological_rules': 'CD: NumType=Card',
                            'decision_factors': ['Counting', 'Quantity', 'Amount']
                        },
                        {
                            'choice': 'Use CD (Ordinal)',
                            'xpos': 'CD',
                            'feats': 'NumType=Ord',
                            'when': 'For ordering or ranking',
                            'examples': [
                                'Third place (third=CD, NumType=Ord)',
                                'First time (first=CD, NumType=Ord)',
                                'Fifth floor (fifth=CD, NumType=Ord)'
                            ],
                            'morphological_rules': 'CD: NumType=Ord',
                            'decision_factors': ['Ordering', 'Ranking', 'Sequence']
                        }
                    ]
                }
            ]
        },
        'PARTICLE_analysis': {
            'title': 'PARTICLE Complete Analysis (RP)',
            'description': 'Complete particle selection with polarity',
            'upos': 'PART',
            'xpos_tags': ['RP'],
            'scenarios': [
                {
                    'context': 'Polarity Selection',
                    'question': 'Should I use negative or positive particle?',
                    'recommendations': [
                        {
                            'choice': 'Use RP (Negative)',
                            'xpos': 'RP',
                            'feats': 'Polarity=Neg',
                            'when': 'For negative particles',
                            'examples': [
                                'Not going (not=RP, Polarity=Neg)',
                                'Never again (never=RP, Polarity=Neg)',
                                "Don't do it (n't=RP, Polarity=Neg)"
                            ],
                            'morphological_rules': 'RP: Polarity=Neg',
                            'decision_factors': ['Negation', 'Denial', 'Prohibition']
                        },
                        {
                            'choice': 'Use RP (Positive)',
                            'xpos': 'RP',
                            'feats': 'Polarity=Pos',
                            'when': 'For positive particles',
                            'examples': [
                                'Yes indeed (yes=RP, Polarity=Pos)',
                                'Do come (do=RP, Polarity=Pos)',
                                'Please help (please=RP, Polarity=Pos)'
                            ],
                            'morphological_rules': 'RP: Polarity=Pos',
                            'decision_factors': ['Affirmation', 'Emphasis', 'Politeness']
                        }
                    ]
                }
            ]
        }
    }

# Initialize session state
if 'selected_recommendations' not in st.session_state:
    st.session_state.selected_recommendations = []

def main():
    st.title("🧠 Complete UD Morphological Decision Support")
    st.markdown("**Comprehensive Universal Dependencies Analysis** - Complete morphological decision making with all features")
    
    decisions = load_complete_morphology_data()
    
    # Sidebar
    with st.sidebar:
        st.header("📋 Select Analysis Type")
        
        decision_options = {key: data['title'] for key, data in decisions.items()}
        selected_key = st.selectbox(
            "Choose analysis type:",
            options=[''] + list(decision_options.keys()),
            format_func=lambda x: "-- Select --" if x == '' else decision_options[x]
        )
        
        if selected_key:
            st.success(f"✅ Selected")
            
        # Show selection count
        if st.session_state.selected_recommendations:
            st.info(f"📌 Selected: {len(st.session_state.selected_recommendations)}")
            
            if st.button("🗑️ Clear All"):
                st.session_state.selected_recommendations = []
                st.rerun()
                
            if st.button("📋 Copy Selected"):
                copy_text = generate_copy_text()
                st.code(copy_text, language="text")
                st.success("✅ Copy the text above!")

    # Main content
    if not selected_key:
        st.info("👆 Please select an analysis type from the sidebar")
        
        st.header("📚 Available Analysis Types")
        
        # Show feature overview
        cols = st.columns(2)
        for i, (key, data) in enumerate(decisions.items()):
            with cols[i % 2]:
                with st.expander(f"🎯 {data['title']}"):
                    st.write(f"**UPOS:** {data['upos']}")
                    st.write(f"**XPOS:** {' • '.join(data['xpos_tags'])}")
                    st.write(f"**Description:** {data['description']}")
        
        # Feature matrix
        st.header("📊 Morphological Features")
        feature_info = {
            'VERB': 'Honorificity=Yes/No, Tense, Aspect, Mood, Voice',
            'ADV': 'AdvType=Manner/Temporal/Locative/Frequentative/Resultative',
            'CONJ': 'ConjType=Coordinating/Correlative/Subordinating',
            'PRON': 'Honorificity=Yes/No, Person, Number, Case'
        }
        
        for upos, features in feature_info.items():
            st.markdown(f"**{upos}:** {features}")
    
    else:
        decision_data = decisions[selected_key]
        
        # Header
        st.header(f"🎯 {decision_data['title']}")
        st.write(decision_data['description'])
        
        col1, col2 = st.columns(2)
        with col1:
            st.info(f"**UPOS:** {decision_data['upos']}")
        with col2:
            st.info(f"**XPOS:** {' • '.join(decision_data['xpos_tags'])}")
        
        st.markdown("---")
        
        # Scenarios
        for scenario_idx, scenario in enumerate(decision_data['scenarios']):
            st.subheader(f"📍 {scenario['context']}")
            st.markdown(f"**❓ {scenario['question']}**")
            
            # Recommendations
            for rec_idx, rec in enumerate(scenario['recommendations']):
                unique_id = f"{selected_key}_{scenario_idx}_{rec_idx}"
                
                with st.container():
                    # Checkbox
                    is_selected = st.checkbox(
                        f"**{rec['choice']}**",
                        key=f"checkbox_{unique_id}",
                        value=any(r['id'] == unique_id for r in st.session_state.selected_recommendations)
                    )
                    
                    # Handle selection
                    if is_selected:
                        rec_data = {
                            'id': unique_id,
                            'decision_type': decision_data['title'],
                            'upos': decision_data['upos'],
                            'context': scenario['context'],
                            'question': scenario['question'],
                            'choice': rec['choice'],
                            'xpos': rec['xpos'],
                            'feats': rec['feats'],
                            'when': rec['when'],
                            'examples': rec['examples'],
                            'rules': rec['morphological_rules'],
                            'decision_factors': rec.get('decision_factors', []),
                            'xpos_tags': decision_data['xpos_tags']
                        }
                        
                        if not any(r['id'] == unique_id for r in st.session_state.selected_recommendations):
                            st.session_state.selected_recommendations.append(rec_data)
                    else:
                        st.session_state.selected_recommendations = [
                            r for r in st.session_state.selected_recommendations if r['id'] != unique_id
                        ]
                    
                    # UD format display
                    st.code(f"{decision_data['upos']} {rec['xpos']} {rec['feats']}", language="text")
                    
                    # Details in expandable section
                    with st.expander("📋 View Details"):
                        st.markdown(f"**When to use:** {rec['when']}")
                        
                        # Decision factors
                        if rec.get('decision_factors'):
                            st.markdown("**🎯 Decision Factors:**")
                            for factor in rec['decision_factors']:
                                st.write(f"• {factor}")
                        
                        # Examples
                        st.markdown("**📝 Examples:**")
                        for example in rec['examples']:
                            st.code(example, language="text")
                        
                        # Morphological rule
                        st.markdown("**🔧 Morphological Rule:**")
                        st.code(rec['morphological_rules'], language="text")
                    
                    st.markdown("---")

def generate_copy_text():
    if not st.session_state.selected_recommendations:
        return "No recommendations selected."
    
    copy_text = "COMPLETE UD MORPHOLOGICAL ANALYSIS\n"
    copy_text += "=" * 50 + "\n\n"
    
    # Group by decision type
    grouped = {}
    for rec in st.session_state.selected_recommendations:
        decision_type = rec['decision_type']
        if decision_type not in grouped:
            grouped[decision_type] = []
        grouped[decision_type].append(rec)
    
    for decision_type, recs in grouped.items():
        copy_text += f"🎯 {decision_type}\n"
        copy_text += "-" * len(decision_type) + "\n\n"
        
        for i, rec in enumerate(recs, 1):
            copy_text += f"{i}. {rec['choice']}\n"
            copy_text += f"   UD Format: {rec['upos']} {rec['xpos']} {rec['feats']}\n"
            copy_text += f"   Context: {rec['context']}\n"
            copy_text += f"   When to use: {rec['when']}\n\n"
            
            # Decision factors
            if rec.get('decision_factors'):
                copy_text += f"   Decision Factors:\n"
                for factor in rec['decision_factors']:
                    copy_text += f"   • {factor}\n"
                copy_text += "\n"
            
            # Examples
            copy_text += f"   Examples:\n"
            for ex in rec['examples']:
                copy_text += f"   • {ex}\n"
            
            copy_text += f"\n   Morphological Rule: {rec['rules']}\n"
            copy_text += "\n" + "-" * 40 + "\n\n"
        
        copy_text += "=" * 50 + "\n\n"
    
    copy_text += f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    copy_text += "Total Selected: " + str(len(st.session_state.selected_recommendations)) + " recommendations\n"
    
    return copy_text

if __name__ == "__main__":
    main()

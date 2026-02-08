"""
Product Inference Engine - AI-powered product recommendation
"""
import re
from typing import List, Dict, Tuple
from loguru import logger


class ProductInferenceEngine:
    """Infer HPCL product needs from text signals"""
    
    def __init__(self):
        # HPCL Product Catalog with keywords
        self.product_keywords = {
            # Industrial Fuels
            "FO": {
                "keywords": ["furnace oil", "fuel oil", "fo ", "heavy fuel", "boiler fuel", "industrial fuel"],
                "equipment": ["boiler", "furnace", "kiln", "dryer", "thermal power"],
                "industries": ["power", "textile", "ceramic", "steel", "cement"]
            },
            "HSD": {
                "keywords": ["high speed diesel", "hsd", "diesel", "auto diesel"],
                "equipment": ["generator", "genset", "diesel generator", "dgset", "vehicle", "truck"],
                "industries": ["logistics", "transport", "construction", "mining", "power backup"]
            },
            "LDO": {
                "keywords": ["light diesel oil", "ldo", "light fuel"],
                "equipment": ["furnace", "dryer", "small boiler"],
                "industries": ["small industry", "tea estate", "food processing"]
            },
            "LSHS": {
                "keywords": ["low sulphur heavy stock", "lshs", "low sulfur fuel", "marine fuel"],
                "equipment": ["ship", "vessel", "marine engine"],
                "industries": ["shipping", "marine", "port"]
            },
            "SKO": {
                "keywords": ["superior kerosene oil", "sko", "kerosene"],
                "equipment": ["burner", "lamp", "heater"],
                "industries": ["domestic", "rural", "heating"]
            },
            
            # Specialty Products
            "Hexane": {
                "keywords": ["hexane", "n-hexane", "solvent extraction"],
                "equipment": ["extraction unit", "solvent plant"],
                "industries": ["edible oil", "vegetable oil", "oil extraction", "solvent extraction"]
            },
            "Solvent 1425": {
                "keywords": ["solvent 1425", "mineral spirits", "paint solvent"],
                "equipment": ["paint plant", "coating unit"],
                "industries": ["paint", "coating", "ink", "resin"]
            },
            "Mineral Turpentine Oil": {
                "keywords": ["mineral turpentine", "mto", "turpentine oil", "white spirit"],
                "equipment": ["paint mixer", "thinner unit"],
                "industries": ["paint", "varnish", "polish", "cleaning"]
            },
            "Jute Batch Oil": {
                "keywords": ["jute batching oil", "jbo", "jute oil", "batching oil"],
                "equipment": ["jute mill", "textile machinery"],
                "industries": ["jute", "textile", "jute processing"]
            },
            
            # Other DS Products
            "Bitumen": {
                "keywords": ["bitumen", "asphalt", "road tar", "paving material"],
                "equipment": ["paver", "road roller", "hot mix plant"],
                "industries": ["road construction", "highway", "infrastructure", "roofing"]
            },
            "Marine Bunker Fuel": {
                "keywords": ["bunker fuel", "marine diesel", "ship fuel", "bunker oil"],
                "equipment": ["ship", "vessel", "tanker", "cargo ship"],
                "industries": ["shipping", "marine", "port operations"]
            },
            "Sulphur": {
                "keywords": ["sulphur", "sulfur", "molten sulphur", "elemental sulfur"],
                "equipment": ["chemical reactor", "fertilizer plant"],
                "industries": ["fertilizer", "chemical", "acid manufacturing"]
            },
            "Propylene": {
                "keywords": ["propylene", "propene", "polypropylene feedstock"],
                "equipment": ["polymerization unit", "chemical reactor"],
                "industries": ["petrochemical", "plastic", "polymer"]
            }
        }
        
        # Operational cues that signal product need
        self.operational_cues = {
            "power_generation": ["power plant", "captive power", "cogeneration", "thermal power"],
            "manufacturing": ["manufacturing plant", "factory", "production unit", "industrial unit"],
            "expansion": ["expansion", "new plant", "commissioning", "setting up", "greenfield"],
            "procurement": ["tender", "procurement", "supply", "quotation", "rfq", "bid"]
        }
    
    def analyze_text(self, text: str) -> Dict:
        """
        Analyze text and extract product signals
        
        Returns:
            {
                'recommended_products': [{'product': 'FO', 'confidence': 0.85, 'reason': '...'}],
                'detected_keywords': ['furnace oil', 'boiler'],
                'detected_equipment': ['boiler', 'furnace'],
                'intent_strength': 'high',
                'urgency_score': 0.8
            }
        """
        text_lower = text.lower()
        
        # Extract signals
        detected_keywords = []
        detected_equipment = []
        product_scores = {}
        
        # Analyze each product
        for product, data in self.product_keywords.items():
            score = 0
            reasons = []
            
            # Check direct keywords
            for keyword in data["keywords"]:
                if keyword.lower() in text_lower:
                    score += 0.4
                    detected_keywords.append(keyword)
                    reasons.append(f"Mentioned '{keyword}'")
            
            # Check equipment signals
            for equipment in data["equipment"]:
                if equipment.lower() in text_lower:
                    score += 0.3
                    detected_equipment.append(equipment)
                    reasons.append(f"Equipment: '{equipment}' detected")
            
            # Check industry context
            for industry in data["industries"]:
                if industry.lower() in text_lower:
                    score += 0.2
                    reasons.append(f"Industry: '{industry}' match")
            
            if score > 0:
                product_scores[product] = {
                    'score': min(score, 1.0),  # Cap at 1.0
                    'reasons': reasons
                }
        
        # Get top 3 recommendations
        sorted_products = sorted(
            product_scores.items(), 
            key=lambda x: x[1]['score'], 
            reverse=True
        )[:3]
        
        recommended_products = [
            {
                'product': product,
                'confidence': round(data['score'], 2),
                'reason': '; '.join(data['reasons'])
            }
            for product, data in sorted_products
        ]
        
        # Determine intent strength
        intent_strength = self._calculate_intent_strength(text_lower)
        
        # Calculate urgency
        urgency_score = self._calculate_urgency(text_lower)
        
        return {
            'recommended_products': recommended_products,
            'detected_keywords': list(set(detected_keywords)),
            'detected_equipment': list(set(detected_equipment)),
            'intent_strength': intent_strength,
            'urgency_score': urgency_score
        }
    
    def _calculate_intent_strength(self, text: str) -> str:
        """Calculate intent strength based on signal type"""
        high_intent_keywords = ["tender", "rfq", "quotation", "procurement", "bid", "supply required"]
        medium_intent_keywords = ["expansion", "new plant", "commissioning", "setting up"]
        
        # Count matches
        high_count = sum(1 for kw in high_intent_keywords if kw in text)
        medium_count = sum(1 for kw in medium_intent_keywords if kw in text)
        
        if high_count > 0:
            return "high"
        elif medium_count > 0:
            return "medium"
        else:
            return "low"
    
    def _calculate_urgency(self, text: str) -> float:
        """Calculate urgency score (0-1)"""
        urgency_keywords = {
            "immediate": 1.0,
            "urgent": 0.9,
            "asap": 0.9,
            "this month": 0.8,
            "tender": 0.7,
            "deadline": 0.7,
            "soon": 0.6,
            "upcoming": 0.5
        }
        
        max_urgency = 0.0
        for keyword, score in urgency_keywords.items():
            if keyword in text:
                max_urgency = max(max_urgency, score)
        
        return max_urgency
    
    def calculate_lead_score(self, analysis: Dict, company_size: str = "medium") -> float:
        """
        Calculate composite lead score (0-100)
        
        Factors:
        - Product confidence
        - Intent strength
        - Urgency
        - Company size
        """
        # Base score from product confidence
        if analysis['recommended_products']:
            avg_confidence = sum(p['confidence'] for p in analysis['recommended_products']) / len(analysis['recommended_products'])
            confidence_score = avg_confidence * 40  # Max 40 points
        else:
            confidence_score = 0
        
        # Intent strength score
        intent_scores = {"high": 30, "medium": 20, "low": 10}
        intent_score = intent_scores.get(analysis['intent_strength'], 10)
        
        # Urgency score
        urgency_score = analysis['urgency_score'] * 20  # Max 20 points
        
        # Company size score
        size_scores = {"enterprise": 10, "large": 8, "medium": 6, "small": 4}
        size_score = size_scores.get(company_size, 6)
        
        # Total score
        total_score = confidence_score + intent_score + urgency_score + size_score
        
        return round(min(total_score, 100), 2)
    
    def extract_location(self, text: str) -> List[str]:
        """Extract location mentions from text"""
        # Common Indian states
        states = [
            "Maharashtra", "Gujarat", "Tamil Nadu", "Karnataka", "Delhi", "Uttar Pradesh",
            "West Bengal", "Rajasthan", "Madhya Pradesh", "Andhra Pradesh", "Telangana",
            "Kerala", "Punjab", "Haryana", "Bihar", "Odisha", "Assam", "Jharkhand"
        ]
        
        found_locations = []
        text_lower = text.lower()
        
        for state in states:
            if state.lower() in text_lower:
                found_locations.append(state)
        
        return found_locations
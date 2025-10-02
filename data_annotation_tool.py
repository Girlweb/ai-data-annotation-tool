
'Author: Mitchele Jebet'

import json
import csv
from datetime import datetime
import random

class DataAnnotationTool:
    """Main class for data annotation and quality assessment"""
    
    def __init__(self):
        self.annotations = []
        self.quality_scores = []
        self.comparison_results = []
        
    def annotate_image(self, image_id, category, confidence, notes=""):
        """
        Annotate an image with category and confidence level
        
        Args:
            image_id: Unique identifier for the image
            category: Classification category (e.g., 'vehicle', 'person', 'animal')
            confidence: Confidence level (1-5 scale)
            notes: Optional notes about the annotation
        """
        annotation = {
            'image_id': image_id,
            'category': category,
            'confidence': confidence,
            'timestamp': datetime.now().isoformat(),
            'notes': notes
        }
        self.annotations.append(annotation)
        print(f"✓ Annotated image {image_id} as '{category}' (confidence: {confidence}/5)")
        return annotation
    
    def quality_check(self, data_entry, criteria):
        """
        Perform quality assessment on a data entry
        
        Args:
            data_entry: Dictionary containing data to check
            criteria: List of quality criteria to evaluate
        """
        score = 0
        max_score = len(criteria)
        feedback = []
        
        for criterion in criteria:
            if criterion == 'completeness':
                if all(data_entry.values()):
                    score += 1
                    feedback.append("✓ Complete")
                else:
                    feedback.append("✗ Missing data")
                    
            elif criterion == 'format':
                if isinstance(data_entry.get('image_id'), str):
                    score += 1
                    feedback.append("✓ Correct format")
                else:
                    feedback.append("✗ Format issue")
                    
            elif criterion == 'consistency':
                if data_entry.get('confidence') in range(1, 6):
                    score += 1
                    feedback.append("✓ Consistent")
                else:
                    feedback.append("✗ Inconsistent value")
        
        quality_result = {
            'data_entry': data_entry,
            'score': score,
            'max_score': max_score,
            'percentage': (score/max_score)*100,
            'feedback': feedback,
            'timestamp': datetime.now().isoformat()
        }
        
        self.quality_scores.append(quality_result)
        print(f"Quality Score: {score}/{max_score} ({quality_result['percentage']:.1f}%)")
        return quality_result
    
    def pairwise_comparison(self, item_a, item_b, criterion):
        """
        Compare two items and determine which is better based on criterion
        
        Args:
            item_a: First item to compare
            item_b: Second item to compare
            criterion: Criterion for comparison (e.g., 'quality', 'accuracy', 'completeness')
        """
        print(f"\n--- Pairwise Comparison: {criterion} ---")
        print(f"Item A: {item_a}")
        print(f"Item B: {item_b}")
        
        # Simulated comparison logic (in real use, human judgment would be applied)
        winner = random.choice(['A', 'B', 'Tie'])
        
        comparison = {
            'item_a': item_a,
            'item_b': item_b,
            'criterion': criterion,
            'winner': winner,
            'timestamp': datetime.now().isoformat()
        }
        
        self.comparison_results.append(comparison)
        print(f"Result: Item {winner} is better for '{criterion}'")
        return comparison
    
    def consistency_check(self):
        """Check consistency across all annotations"""
        if len(self.annotations) < 2:
            print("Need at least 2 annotations for consistency check")
            return None
        
        categories = [a['category'] for a in self.annotations]
        confidences = [a['confidence'] for a in self.annotations]
        
        consistency_report = {
            'total_annotations': len(self.annotations),
            'unique_categories': len(set(categories)),
            'avg_confidence': sum(confidences) / len(confidences),
            'consistency_score': None
        }
        
        # Calculate consistency score
        category_distribution = {}
        for cat in categories:
            category_distribution[cat] = category_distribution.get(cat, 0) + 1
        
        # Higher consistency if categories are well distributed
        consistency_report['category_distribution'] = category_distribution
        consistency_report['consistency_score'] = (
            len(set(categories)) / len(categories) * 100
        )
        
        print("\n=== Consistency Report ===")
        print(f"Total Annotations: {consistency_report['total_annotations']}")
        print(f"Unique Categories: {consistency_report['unique_categories']}")
        print(f"Average Confidence: {consistency_report['avg_confidence']:.2f}/5")
        print(f"Category Distribution: {category_distribution}")
        
        return consistency_report
    
    def generate_report(self, filename='annotation_report.json'):
        """Generate comprehensive report of all annotation work"""
        report = {
            'summary': {
                'total_annotations': len(self.annotations),
                'total_quality_checks': len(self.quality_scores),
                'total_comparisons': len(self.comparison_results),
                'generated_at': datetime.now().isoformat()
            },
            'annotations': self.annotations,
            'quality_scores': self.quality_scores,
            'comparisons': self.comparison_results
        }
        
        # Calculate overall quality
        if self.quality_scores:
            avg_quality = sum(q['percentage'] for q in self.quality_scores) / len(self.quality_scores)
            report['summary']['average_quality_score'] = f"{avg_quality:.2f}%"
        
        # Save to JSON
        with open(filename, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"\n✓ Report saved to {filename}")
        return report
    
    def export_to_csv(self, filename='annotations.csv'):
        """Export annotations to CSV format"""
        if not self.annotations:
            print("No annotations to export")
            return
        
        with open(filename, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=self.annotations[0].keys())
            writer.writeheader()
            writer.writerows(self.annotations)
        
        print(f"✓ Annotations exported to {filename}")


def demo_workflow():
    """Demonstrate a complete data annotation workflow"""
    print("=" * 60)
    print("AI DATA ANNOTATION & QUALITY ASSESSMENT TOOL")
    print("Portfolio Project by Mitchele Jebet")
    print("=" * 60)
    
    tool = DataAnnotationTool()
    
    # Simulate image annotation tasks
    print("\n--- TASK 1: Image Classification ---")
    tool.annotate_image("IMG_001", "vehicle", 5, "Clear image of a car")
    tool.annotate_image("IMG_002", "person", 4, "Person in good lighting")
    tool.annotate_image("IMG_003", "animal", 5, "Dog clearly visible")
    tool.annotate_image("IMG_004", "building", 4, "Office building, slight blur")
    tool.annotate_image("IMG_005", "vehicle", 5, "Truck, side view")
    
    # Quality assessment
    print("\n--- TASK 2: Quality Assessment ---")
    for annotation in tool.annotations[:3]:
        tool.quality_check(
            annotation, 
            ['completeness', 'format', 'consistency']
        )
    
    # Pairwise comparisons
    print("\n--- TASK 3: Pairwise Comparisons ---")
    tool.pairwise_comparison(
        "Annotation with detailed notes",
        "Annotation with minimal notes",
        "completeness"
    )
    tool.pairwise_comparison(
        "High confidence classification",
        "Low confidence classification",
        "reliability"
    )
    
    # Consistency check
    print("\n--- TASK 4: Consistency Analysis ---")
    tool.consistency_check()
    
    # Generate reports
    print("\n--- TASK 5: Report Generation ---")
    report = tool.generate_report()
    tool.export_to_csv()
    
    # Display summary statistics
    print("\n" + "=" * 60)
    print("SUMMARY STATISTICS")
    print("=" * 60)
    print(f"Total Annotations: {len(tool.annotations)}")
    print(f"Quality Checks Performed: {len(tool.quality_scores)}")
    print(f"Comparisons Completed: {len(tool.comparison_results)}")
    
    if tool.quality_scores:
        avg_quality = sum(q['percentage'] for q in tool.quality_scores) / len(tool.quality_scores)
        print(f"Average Quality Score: {avg_quality:.2f}%")
    
    print("\n✓ Demo completed successfully!")
    print("Files generated: annotation_report.json, annotations.csv")
    print("=" * 60)


# Example usage for custom annotation tasks
def custom_annotation_example():
    """Example of how to use the tool for custom tasks"""
    tool = DataAnnotationTool()
    
    # Custom image annotations
    images_to_annotate = [
        {"id": "IMG_100", "category": "landscape", "confidence": 5},
        {"id": "IMG_101", "category": "portrait", "confidence": 4},
        {"id": "IMG_102", "category": "food", "confidence": 5},
    ]
    
    for img in images_to_annotate:
        tool.annotate_image(img["id"], img["category"], img["confidence"])
    
    # Generate report
    tool.generate_report('custom_report.json')
    tool.export_to_csv('custom_annotations.csv')


if __name__ == "__main__":
    # Run the demonstration workflow
    demo_workflow()
    
    print("\n\nTo run custom annotations, uncomment the line below:")
    print("# custom_annotation_example()")

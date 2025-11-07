# Data Parser Contract

**Service**: Data Parser  
**Purpose**: Load and normalize JSON archive data into Python data models  
**Implements**: FR-001, FR-002

## Interface

```python
def load_archive(json_file_path: str) -> List[Meeting]:
    """
    Load and parse JSON archive file into normalized Meeting objects.
    
    Args:
        json_file_path: Path to meeting-summaries-array-3.json
        
    Returns:
        List of normalized Meeting objects
        
    Raises:
        FileNotFoundError: If JSON file doesn't exist
        json.JSONDecodeError: If JSON is malformed
        ValueError: If required fields are missing
    """
    pass

def normalize_meeting(raw_meeting: dict) -> Meeting:
    """
    Normalize a raw meeting dictionary into a Meeting object.
    
    Args:
        raw_meeting: Raw meeting dictionary from JSON
        
    Returns:
        Normalized Meeting object
        
    Raises:
        ValueError: If required fields are missing or invalid
    """
    pass
```

## Contract Tests

1. **Valid JSON parsing**: Parse valid JSON file returns list of Meeting objects
2. **Missing optional fields**: Missing optional fields handled gracefully (empty lists, None values)
3. **Date parsing**: ISO dates (YYYY-MM-DD) parsed correctly to datetime objects
4. **String parsing**: Comma-separated strings (peoplePresent, topicsCovered) parsed to lists
5. **Name normalization**: Name variations handled consistently
6. **Error handling**: Malformed meetings logged and skipped, processing continues
7. **Attribution preservation**: host and documenter fields preserved in Meeting objects

## Performance Requirements

- Parse 120 meetings in < 1 second
- Parse 10,000 meetings in < 10 seconds (SC-009)


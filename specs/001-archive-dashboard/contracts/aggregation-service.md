# Aggregation Service Contract

**Service**: Aggregation Service  
**Purpose**: Aggregate decisions and action items from all meetings  
**Implements**: FR-011, FR-012

## Interface

```python
def aggregate_decisions(meetings: List[Meeting]) -> List[Decision]:
    """
    Aggregate all decisions from all meetings with workgroup and date context.
    
    Args:
        meetings: List of Meeting objects
        
    Returns:
        List of Decision objects with workgroup and date from parent meeting
    """
    pass

def aggregate_action_items(meetings: List[Meeting]) -> List[ActionItem]:
    """
    Aggregate all action items from all meetings with workgroup and date context.
    
    Args:
        meetings: List of Meeting objects
        
    Returns:
        List of ActionItem objects with workgroup and date from parent meeting
    """
    pass
```

## Contract Tests

1. **Decision aggregation**: All decisions from all meetings included in result
2. **Action item aggregation**: All action items from all meetings included in result
3. **Context preservation**: Decisions and action items include workgroup and date from parent meeting
4. **Empty meetings**: Empty meetings list returns empty aggregation lists
5. **Meetings without decisions**: Meetings without decisions don't cause errors
6. **Meetings without action items**: Meetings without action items don't cause errors
7. **Performance**: Aggregating 10,000 meetings completes in < 5 seconds (SC-004)

## Performance Requirements

- Aggregate decisions and action items: < 5 seconds (SC-004)


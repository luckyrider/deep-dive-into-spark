# Coding Skills

## Coding Style Tips


## Implementation Tips

### SparkFirehoseListener

This is a concrete Java class in order to ensure that we don't forget to update it when adding new methods to SparkListener: forgetting to add a method will result in a compilation error (if this was a concrete Scala class, default implementations of new event handlers would be inherited from the SparkListener trait).

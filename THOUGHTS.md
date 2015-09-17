# Recruiting tast
This is my solution for the backend recruiting task.
More details on the problem can be found in the [readme](README.md) file.

Please find details below on my design decisions and other instructions.

# Solution
The initial naive idea is the simplest possible: read the input coordinates and distance and check all the existing stores. That, obviously, is quickly ruled out if a data size is big (or at least significant enough). So I took off the shelf my algorithms book and found out that the problem stament looks a lot like a range spartial search.

From that on I researched a little bit about KD-Tree (the data structure used to implement the range search in this case) and then how I could use it. Turns out scipy implements it. And it also implements the search range function within a radius. Yay! The only issue is that it uses cartesian coordinates whilst all the inputs are in latitudes and longitues (scipy doesn't allow me to change the "distance function" - that would avoid all the conversions back and forth). 

Fortunately coordinates to xyz conversion a [known problem](https://en.wikipedia.org/wiki/ECEF). After that the only problem was knowing how to convert the distance to a distance in the plane (or, as I learned, great circle distance to euclidean distance). Also another [known problem](https://en.wikipedia.org/wiki/Great-circle_distance) with [explanations](http://www.had2know.com/academics/great-circle-distance-sphere-2-points.html). That basically solves the problem. It is also possible to find multiple python references online with implementations

So the algorithm turns out to be:
- Load all data;
- Convert coordinates to xyz and add to the tree;
- For each query:
    - Check the stores that have the desired tags.    
    - Convert the query coordinates to xyz.
    - Convert the distance to euclidean distance.

# Python
I've tried to make my code as pythonist as possible (I haven't done python in a long time). I believe there are still a few places I'm missing, but I've tried to do it as close as possible within the time frame.

# Points for improvement
- Fix the returned error messages (current client doesn't display the errors). Right now for input validation errors, the server just throws an internal exception whose message is not sent back.'
- Suggest tags if there is a typo (for better accuracy).
- Documentation?
- More code comments?

# Assumptions
Hopefully the tests cover (and explain) my assumptions. But...
- The same product can be on the results as it can happen in different stores (and even within the same store - product_id seems to vary).
- Height is always zero (for coordinates conversion).


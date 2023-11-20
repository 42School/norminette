struct {
	// points is to something
	int	points; // is an int :D
};

typedef /* oopss */ bool bool;

enum test {
    // blaboe
    hello,  // it works
    /* error*/ error
};

void hello(/* nothing */ void) // error because comment is in middle of the line
{
   // error because scope is from a function
   {
      // are you trying to cheat?
      // error because scope is from a function
   }
}

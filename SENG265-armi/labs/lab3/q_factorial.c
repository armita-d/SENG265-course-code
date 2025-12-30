#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[])
{

    /*
     * variable to store the final answer
     */
   long long int factorial = 1;

    /*
     * WRITE YOUR CODE TO DO COMMAND LINE INPUT CHECKING HERE
     */
     if (argc !=2) {
        printf("Usage: %s <non-negative integer>\n", argv[0]);
        return 1;
     }
    /*
     * Takes the command line input and converts it into int.
     */
    int num = atoi(argv[1]);
    if(num < 0) {
      printf("Error: factorial is not defined for negative numbers.\n");
      return 1;
    }

    /*
     * WRITE YOUR CODE TO DO THE FACTORIAL CALCULATIONS HERE
     */
     for (int i= 1; i<= num; i++) {
         factorial *= i;
     }
      printf("%lld\n", factorial);
   // printf("%d\n", factorial);
}

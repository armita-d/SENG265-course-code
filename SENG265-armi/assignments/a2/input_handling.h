#ifndef _INPUT_HANDLING_H_
#define _INPUT_HANDLING_H_

/* add your include and prototypes here*/
/*this file declares all functions resposible for reading and processing survey input data, including questions, opyions, and participant responses.
*/
#include "dyn_survey.h"

void read_questions(char *line, char **questions, int *num_questions);
void read_options(char *line, char **options, int *num_options);
int find_opt(char *resp, char **options, int num_options);
void process_responses(char *line, Response *responses, int response_index, char **programs, int num_programs, char **residence_statuses, int num_statuses, char **options, int num_options, int num_questions);


#endif

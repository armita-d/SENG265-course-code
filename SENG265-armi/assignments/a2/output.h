#ifndef _OUTPUT_H_
#define _OUTPUT_H_

/* add your include and prototypes here*/
#include "dyn_survey.h"

void print_survey_header(int total_responses);
void print_frequencies(int **freq, char **questions, char **options, int num_questions, int num_options, int total_responses);
void print_averages(double *averages, char **questions, int num_questions);
void print_demographic_stats(double *program_stats, double *residence_stats, char **programs, int num_programs, char **residence_statuses, int num_statuses);
void print_analysis(SurveyConfig config, int **freq, double *averages, double *program_stats, double *residence_stats, char **questions, char **options, char **programs, char **residence_statuses, int num_questions, int num_options, int num_programs, int num_statuses, int total_responses);


#endif

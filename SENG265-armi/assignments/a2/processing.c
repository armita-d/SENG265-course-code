/* processing.c */
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include "processing.h"
/*this file contains functions that precess raw survey data to compute
*1.response freq for each Q and option
*2.avg response scores
*3.demographic statistics (program and residence status)
*/
//calculate freq:count how many respondents selected each option for each Q
void calculate_frequencies(int **freq, Response *responses, int total_responses, int num_questions, int num_options) {
    for (int i = 0; i < total_responses; i++) {
        for (int q = 0; q < num_questions; q++) {
            int answer_val = responses[i].answers[q];
            if (answer_val >= 0 && answer_val < num_options) {
                freq[q][answer_val]++;
            }
        }
    }
}
//compute the avg response value for each Q
void calculate_averages(double *averages, int **freq, int total_responses, int num_questions, int num_options) {
    for (int i = 0; i < num_questions; i++) {
        double sum = 0;
        for (int j = 0; j < num_options; j++) {
            sum += freq[i][j] * (j + 1);
        }
        if (total_responses > 0) {
            averages[i] = sum / total_responses;
        }
    }
}
//determine the percentage distribution of respondents by program and residence status.
void calculate_demographic_stats(double *program_stats, double *residence_stats, Response *responses, int total_responses, char **programs, int num_programs, char **residence_statuses, int num_statuses) {
    for (int i = 0; i < num_programs; i++) {
        program_stats[i] = 0;
    }
    for (int i = 0; i < num_statuses; i++) {
        residence_stats[i] = 0;
    }
    
    for (int i = 0; i < total_responses; i++) {
        for (int p = 0; p < num_programs; p++) {
            if (strcmp(responses[i].respondent.program, programs[p]) == 0) {
                program_stats[p]++;
                break;
            }
        }
        for (int r = 0; r < num_statuses; r++) {
            if (strcmp(responses[i].respondent.residence_status, residence_statuses[r]) == 0) {
                residence_stats[r]++;
                break;
            }
        }
    }
    
    for (int i = 0; i < num_programs; i++) {
        program_stats[i] = (program_stats[i] / total_responses) * 100.0;
    }
    for (int i = 0; i < num_statuses; i++) {
        residence_stats[i] = (residence_stats[i] / total_responses) * 100.0;
    }
}

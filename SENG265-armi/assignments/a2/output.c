/* output.c */
#include <stdio.h>
#include "output.h"
/*this file handels all formatted output for the survey analysis program.
*it printsheadears, freq tables, avgs and demographic statistics based on
*the processed survey data.
*/
/*prints main survey header, including the total number of respondents
* who participated in the survey. 
*/
void print_survey_header(int total) {
    printf("ECS Student Survey\nSURVEY RESPONSE STATISTICS\n\nNUMBER OF RESPONDENTS: %d\n\n", total);
}
//print percentage freq for each answer for evety question in survey
void print_frequencies(int **freq, char **questions, char **options, int num_questions, int num_options, int total) {
    printf("#####\nFOR EACH QUESTION/ASSERTION BELOW, RELATIVE PERCENTUAL FREQUENCIES ARE COMPUTED FOR EACH LEVEL OF AGREEMENT\n\n");
    for (int i=0; i<num_questions; i++) {
        printf("%d. %s\n", i+1, questions[i]);
        for (int j=0; j<num_options; j++) {
            printf("%.2f: %s\n", total ? freq[i][j]*100.0/total : 0.0, options[j]);
        }
        if (i < num_questions-1) {
            printf("\n");
        }
    }
}
//prints the avg responses for each question
void print_averages(double *averages, char **questions, int num_questions) {
    printf("#####\nFOR EACH QUESTION/ASSERTION BELOW, THE AVERAGE RESPONSE IS SHOWN (FROM 1-DISAGREEMENT TO 4-AGREEMENT)\n\n");
    for (int i=0;i<num_questions;i++){
        printf("%d. %s - %.2f\n", i + 1, questions[i], averages[i]);
    }
}
//print demographic statistics the percentage of resposdents in each program
//and each residence status category
void print_demographic_stats(double *program_stats, double *residence_stats, char **programs, int num_programs, char **residence_statuses, int num_statuses) {
    printf("#####\nFOR EACH DEMOGRAPHIC CATEGORY BELOW, RELATIVE PERCENTUAL FREQUENCIES ARE COMPUTED FOR EACH ATTRIBUTE VALUE\n\n");
    printf("UNDERGRADUATE PROGRAM\n");
    for (int i=0; i<num_programs; i++) {
        printf("%.2f: %s\n", program_stats[i], programs[i]);
    }
    printf("\nRESIDENCE STATUS\n");
    for (int i=0; i<num_statuses; i++) {
        printf("%.2f: %s\n", residence_stats[i], residence_statuses[i]);
    }
}
//centeral output controller
void print_analysis(SurveyConfig config, int **freq, double *averages, double *program_stats, double *residence_stats, char **questions, char **options, char **programs, char **residence_statuses, int num_questions, int num_options, int num_programs, int num_statuses, int total) {
    print_survey_header(total);
    if (config.show_freq) {
        print_frequencies(freq, questions, options, num_questions, num_options, total);
    }
    if (config.show_avg) {
        if (config.show_freq){
            printf("\n");
        }
       
        print_averages(averages, questions, num_questions);
    }
    if (config.show_demographics) {
        if (config.show_freq || config.show_avg) {
            printf("\n");
        }
        print_demographic_stats(program_stats, residence_stats, programs, num_programs, residence_statuses, num_statuses);
    }
}

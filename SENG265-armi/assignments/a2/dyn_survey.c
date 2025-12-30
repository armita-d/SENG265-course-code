/*this program reads survey configuration, question, answer options
* and student responses from stdin it dynamically allocates memory for all 
*data structures, calculates statistics such as freq, avg and demographic distribution
*and prints the analysis to stdout.
*
*the helper funcs:
*input_handling.h: reading question and options
*processing.h: calculating statistics
*output.h: printing result
*emalloc.h: safe memory alocation.
*/
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include "dyn_survey.h"
#include "input_handling.h"
#include "output.h"
#include "emalloc.h"
#include "processing.h"

/*
*main: entry point of survey program
*reads all the input data, dynamically
* calculates statictics, print results, and free allocated memory.
*return 0 on succesfull compltiation.
*/
int main() {
    char line[1024];//buffer for reading input lines
    //* points to a single  var or the firts elements of an array
   //** points to a pointer
    char **questions = NULL;
    char **options = NULL;
    char **programs = NULL;
    char **residence_statuses = NULL;
    Response *responses = NULL;
    int **freq = NULL;
    double *averages = NULL;
    double *program_stats = NULL;
    double *residence_stats = NULL;
    //counters and flags: counters track quantitties and flags show which statistics(freq, avg_
    int num_questions = 0, num_options = 0, total = 0;
    int num_programs = 0, num_statuses = 0;
    int show_freq = 0, show_avg = 0, show_demographics = 0;
    int step = 0;
    int num_respondents = 0;
    //read input line by line
    while (fgets(line, sizeof(line), stdin)) {
        if (line[0] == '#') continue;//ignore comment lines

        switch (step) {
            case 0://first line:configuration flag(show frq, avg, demograohics)
                sscanf(line, "%d,%d,%d", &show_freq, &show_avg, &show_demographics);
                step = 1;
                break;
            case 1://read undergraduate programs
                programs = (char**)emalloc(8 * sizeof(char*));//we have 8 programs
                for (int i = 0; i < 8; i++) {
                    programs[i] = (char*)emalloc(MAX_LEN * sizeof(char*));
                    programs[i][0]='\0';//initialize empty string
                }
                read_options(line, programs, &num_programs);
                step = 2;
                break;
            case 2://read residence statuses
                residence_statuses = (char**)emalloc(3 * sizeof(char));//3 statues
                for (int i = 0; i < 3; i++) {
                    residence_statuses[i] = (char*)emalloc(MAX_LEN * sizeof(char*));
                    residence_statuses[i][0] ='\0';
                }
                read_options(line, residence_statuses, &num_statuses);
                step = 3;
                break;
            case 3:// read questions
                if (strchr(line, ';')) {
                    char temp_line[1024];
                    strcpy(temp_line, line);
                    char *token = strtok(temp_line, ";\n");
                    while (token) {
                        num_questions++;
                        token = strtok(NULL, ";\n");
                    }
                    //allocate memory for questions
                    questions = (char **)emalloc(num_questions * sizeof(char *));
			for (int i = 0; i < num_questions; i++) {
			    questions[i] = (char *)emalloc(MAX_LEN * sizeof(char));
			    questions[i][0] = '\0';
			}
                        //alocate memory for freq table
			freq = (int **)emalloc(num_questions * sizeof(int *));
				for (int i = 0; i < num_questions; i++) {
				    freq[i] = (int *)emalloc(4 * sizeof(int));//assume 4  options per question
				    for (int j = 0; j < 4; j++) freq[i][j] = 0;
				}
                    //allocate avg array
                    averages = (double*)emalloc(num_questions * sizeof(double));
                    for(int i= 0; i < num_questions;i++) averages[i] =0.0;
                    read_questions(line, questions, &num_questions);
                    step = 4;
                }
                break;
            case 4://read answer options
                if (strchr(line, ',')) {
                    char temp_line[1024];
                    strcpy(temp_line, line);
                    char *token = strtok(temp_line, ",\n");
                    while (token) {
                        num_options++;
                        token = strtok(NULL, ",\n");
                    }
                    //allocate memory for option strings
                    options = (char**)emalloc(num_options * sizeof(char*));
                    for (int i = 0; i < num_options; i++) {
                        options[i] = (char*)emalloc(MAX_LEN * sizeof(char));
                        options[i][0] = '\0';
                    }
                    
                    read_options(line, options, &num_options);
                    step = 5;
                }
                break;
            case 5://read number of respondents and allocate response structs
                sscanf(line, "%d", &num_respondents);
                responses = (Response*)emalloc(num_respondents * sizeof(Response));
                for (int i = 0; i < num_respondents; i++) {
                    responses[i].answers = (int*)emalloc(num_questions * sizeof(int));
                }//allocate arrays for demographic statistics
                program_stats = (double*)emalloc(num_programs * sizeof(double));
                residence_stats = (double*)emalloc(num_statuses * sizeof(double));
                step = 6;
                break;
            case 6://read each respondents's answer and demographics
		if (total < num_respondents) {
    		process_responses(line, responses, total, programs, num_programs, residence_statuses, num_statuses, options, num_options, num_questions);
		total++;
		}                
                break;
        }
    }

    //calculate statistics
    calculate_frequencies(freq, responses, total, num_questions, num_options);
    calculate_averages(averages, freq, total, num_questions, num_options);
    calculate_demographic_stats(program_stats, residence_stats, responses, total, programs, num_programs, residence_statuses, num_statuses);
    //print analysis
    SurveyConfig config = {show_freq, show_avg, show_demographics};
    print_analysis(config, freq, averages, program_stats, residence_stats, questions, options, programs, residence_statuses, num_questions, num_options, num_programs, num_statuses, total);
    //free all dynamically allocated memory
    for (int i = 0; i < num_questions; i++) {
        free(questions[i]);
    }
    free(questions);
    
    for (int i = 0; i < num_options; i++) {
        free(options[i]);
    }
    free(options);
    
    for (int i = 0; i < num_programs; i++) {
        free(programs[i]);
    }
    free(programs);
    
    for (int i = 0; i < num_statuses; i++) {
        free(residence_statuses[i]);
    }
    free(residence_statuses);
    
    for (int i = 0; i < total; i++) {
        free(responses[i].answers);
    }
    free(responses);
    
    for (int i = 0; i < num_questions; i++) {
        free(freq[i]);
    }
    free(freq);
    
    free(averages);
    free(program_stats);
    free(residence_stats);
    
    return 0;//program executed successfully
}

/* input_handling.c */
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include "input_handling.h"

/*this file handels reading and parsing all survey input data.
*it extracts questions, options, and participant responses
*from input lines and stores them in dynamically allocated arrays.
*/

/*
*reads a semicolon_separated line of survey Q and stores
*each Q string in the 'Q' array.
*line: input line containing Q  seprated by ';'
*Q:2D array to store Q strings
*num_questions:pointer to int to store the number of questions read
*/
void read_questions(char *line, char **questions, int *num_questions) {   
    char *token = strtok(line, ";\n");//split line ';' or newline
    int count = 0;
    while (token) { 
        strncpy(questions[count], token, MAX_LEN);//copy token into questions array
        count++;
        token = strtok(NULL, ";\n");
    }
    *num_questions = count;//store total number of question
}

/*
*read a comma-seprated line of survey options(ex:strongly agree,agree,...)
*and stores them in the 'option'array.
*line: input line containing comma-seprated options
*options: 2D array to store option string
*num_options: pointer to int to store the number of option read 
*/
void read_options(char *line, char **options, int *num_options) {
    char *token = strtok(line, ",\n");// split line
    int count = 0;
    while (token) {
        strncpy(options[count], token, MAX_LEN);//copy token into options array
        count++;
        token = strtok(NULL, ",\n");
    }
    *num_options = count;//Stores total number of options parsed
}
//serches for response string in the  options array and returns 
//its index.return -1 if not find.
int find_opt(char *resp, char **options, int num_options) {
    for (int i = 0; i < num_options; i++)
        if (strcmp(resp, options[i]) == 0) return i;//match found
    return -1;//match not found
}
//parse one respondents survey line extracting demographic info(program, residence status)
//and their answers.each response is converted to an int index based on matching opyion.

void process_responses(char *line, Response *responses, int response_index, char **programs, int num_programs, char **residence_statuses, int num_statuses, char **options, int num_options, int num_questions) {
    char *token = strtok(line, ",\n");
    int token_count = 0;
    int answer_index = 0;
    //loop thru tokens representing program, residence and answers
    while (token) {
        if (token_count == 0) {//first token:program name
            strncpy(responses[response_index].respondent.program, token, MAX_LEN);
        } else if (token_count == 1) {//second token:residence status
            strncpy(responses[response_index].respondent.residence_status, token, MAX_LEN);
        } else {//remaining tokens :answer to survey q
            if (answer_index < num_questions) {
                responses[response_index].answers[answer_index] = find_opt(token, options, num_options);
                answer_index++;
            }
        }
        token_count++;
        token = strtok(NULL, ",\n");
    }
}

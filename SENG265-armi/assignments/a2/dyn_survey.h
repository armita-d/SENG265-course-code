/*defines the data struct  for respondents and responses, flags for  survey analysis and
*declares all the func needed to read data, process survey responses, calculate statistics and print the results
*/
#ifndef DYN_SURVEY_H
#define DYN_SURVEY_H
// max len for strings used in questions, options and demographic attributes
#define MAX_LEN 256
// struct to store demographic info of respondent
typedef struct {
    char program[MAX_LEN];// the undergraduate program of the respondent
    char residence_status[MAX_LEN];//the residence status of the respondent
} Respondent;
//struct to store a respondent's data along with their answers
typedef struct {
    Respondent respondent;//demographic info for respondent
    int *answers; //array of int responses for each question
} Response;
// struct  to store configuration flags indicating which statistics to display
typedef struct {
    int show_freq; //flag to indicate if freq should be display
    int show_avg;  //flag to show if  avg should be display
    int show_demographics; //flag to show if demographic  statistics should be display
} SurveyConfig;

//func prototypes for reading questions and options
void read_questions(char *line, char **questions, int *num_questions);
void read_options(char *line, char **options, int *num_options);
void read_demographic_options(char *line, char **programs, int *num_programs, char **residence_statuses, int *num_statuses);
//func to find the index of response in a given list of options
int find_opt(char *resp, char **options, int num_options);
//func to process a single line of responses and store in respomse struct
void process_responses(char *line, Response *responses, int response_index, char **programs, int num_programs, char **residence_statuses, int num_statuses, char **options, int num_options, int num_questions);
//func to calculate statistics
void calculate_frequencies(int **freq, Response *responses, int total_responses, int num_questions, int num_options);
void calculate_averages(double *averages, int **freq, int total_responses, int num_questions, int num_options);
void calculate_demographic_stats(double *program_stats, double *residence_stats, Response *responses, int total_responses, char **programs, int num_programs, char **residence_statuses, int num_statuses);
//func to print results
void print_survey_header(int total_responses);
void print_frequencies(int **freq, char **questions, char **options, int num_questions, int num_options, int total_responses);
void print_averages(double *averages, char **questions, int num_questions);
void print_demographic_stats(double *program_stats, double *residence_stats, char **programs, int num_programs, char **residence_statuses, int num_statuses);
void print_analysis(SurveyConfig config, int **freq, double *averages, double *program_stats, double *residence_stats, char **questions, char **options, char **programs, char **residence_statuses, int num_questions, int num_options, int num_programs, int num_statuses, int total_responses);

#endif

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_QUESTIONS 12
#define MAX_OPTIONS 4
#define MAX_RESPONSES 100
#define MAX_LINE 1024


int answer_value(const char *ans, char*options[]){
    for (int i=0; i < MAX_OPTIONS; i++) {
        if(strcmp(ans, options[i]) == 0) return i + 1;
       }
       return 0;
}

int main() {
    char line[MAX_LINE];
    int show_freq = 0, show_avg = 0;
    char *questions[MAX_QUESTIONS];
    char *answer_options[MAX_OPTIONS];
    int freq[MAX_QUESTIONS][MAX_OPTIONS] = {0};
    int sums[MAX_QUESTIONS] = {0};
    int num_respondents = 0;

    int stage = 0; // 0=flags, 1=questions, 2=options, 3=responses

    while (fgets(line, MAX_LINE, stdin)) {
        line[strcspn(line, "\n")] = 0; // remove newline
        if (line[0] == '#' || strlen(line) == 0) continue;

        if (stage == 0) {
            sscanf(line, "%d,%d", &show_freq, &show_avg);
            stage = 1;
            continue;
        }

        if (stage == 1) {
            int i = 0;
            char *token = strtok(line, ";\n");
            while (token && i < MAX_QUESTIONS) {
                questions[i] = malloc(strlen(token) + 1);
                strcpy(questions[i], token);
                token = strtok(NULL, ";\n");
                i++;
            }
            stage = 2;
            continue;
        }

        if (stage == 2) {
            int i = 0;
            char *token = strtok(line, ",\n");
            while (token && i < MAX_OPTIONS) {
                answer_options[i] = malloc(strlen(token) + 1);
                strcpy(answer_options[i], token);
                token = strtok(NULL, ",\n");
                i++;
            }
            stage = 3;
            continue;
        }

        // Stage 3: responses
        int q = 0;
        char *token = strtok(line, ",\n");
        while (token && q < MAX_QUESTIONS) {
            int a_index = -1;
            for (int i = 0; i < MAX_OPTIONS; i++) {
                if (strcmp(token, answer_options[i]) == 0) {
                    a_index = i;
                    break;
                }
            }
            if (a_index != -1) {
                freq[q][a_index]++;
                sums[q] += (a_index + 1); // numeric value 1-4
            }
            token = strtok(NULL, ",\n");
            q++;
        }
        num_respondents++;
    }

    // Print header
    printf("ECS Student Survey\nSURVEY RESPONSE STATISTICS\n\nNUMBER OF RESPONDENTS: %d\n", num_respondents);

    if (show_freq) {
        printf("\n#####\nFOR EACH QUESTION/ASSERTION BELOW, RELATIVE PERCENTUAL FREQUENCIES ARE COMPUTED FOR EACH LEVEL OF AGREEMENT\n\n");
        for (int q = 0; q < MAX_QUESTIONS; q++) {
            printf("%d. %s\n", q + 1, questions[q]);
            for (int a = 0; a < MAX_OPTIONS; a++) {
                double perc = (num_respondents > 0) ? (freq[q][a] * 100.0 / num_respondents) : 0.0;
                printf("%.2f: %s\n", perc, answer_options[a]);
            }
            if (q < MAX_QUESTIONS -1) printf("\n");
        }
    }

    if (show_avg) {
        printf("\n#####\nFOR EACH QUESTION/ASSERTION BELOW, THE AVERAGE RESPONSE IS SHOWN (FROM 1-DISAGREEMENT TO 4-AGREEMENT)\n\n");
        for (int q = 0; q < MAX_QUESTIONS; q++) {
            double avg = (num_respondents > 0) ? (double)sums[q] / num_respondents : 0.0;
            printf("%d. %s - %.2f\n", q + 1, questions[q], avg);
        }
    }

    // Free memory
    for (int i = 0; i < MAX_QUESTIONS; i++) free(questions[i]);
    for (int i = 0; i < MAX_OPTIONS; i++) free(answer_options[i]);

    return 0;
}

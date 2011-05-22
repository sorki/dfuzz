#include <stdio.h>
#include <string.h>
#include <stdlib.h>

/* Small buffer size sample */

void usage() {
  fprintf(stderr, "Usage: sample -f config_file");
}

int main(int argc, char *argv[])
{
  unsigned int i;
  char * cfg_varname;
  char * cfg_value;
  cfg_varname = malloc(sizeof(char)*10);
  cfg_value = malloc(sizeof(char)*200);
  if(argc != 3) {
    usage();
    return 1;
  }

  if(strcmp(argv[1], "-f") != 0) {
    usage();
    return 1;
  }

  char * filename;
  filename = malloc(sizeof(char)*300);
  strncpy(filename, argv[2], 299);
  printf("Opening %s\n", filename);

  FILE *file = NULL;
  if((file = fopen(filename, "r")) == NULL) {
    fprintf(stderr, "Error opening file '%s'\n", filename);
    return 1;
  }

  while(fscanf(file, "%s %s", cfg_varname, cfg_value) != EOF) { // unsafe operation here
    printf("%s %s\n", cfg_varname, cfg_value);
  }

  printf("Closing %s\n", filename);
  if (file) fclose(file);
  free(cfg_varname);
  free(cfg_value);
  free(filename);
  return 0;
}

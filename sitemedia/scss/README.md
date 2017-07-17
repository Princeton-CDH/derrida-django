# Derrida Sass Assets

## Requirements
These are the requirements needed to compile the styles used by this project.
* [Sass](http://sass-lang.com/)
* [Bourbon](https://github.com/thoughtbot/bourbon)
* [Neat](https://github.com/thoughtbot/neat)

### File Structure
This project depends on Bourbon and Neat libraries to be installed and located in the `sitemedia/scss` folder.
* Bourbon directory: `scss/bourbon`
* Neat directory: `scss/neat`

## Installation

### Sass compiler
Sass is required to compile sass files into web-readable css. There are many ways of compiling sass files; this project uses the sass gem package.

#### Install via gem
Run the command `gem install sass`

### Bourbon and Neat
The easiest way to install Bourbon and Neat is through `gem`. However, you can use any installation method listed in the the Bourbon and Neat documentation as long as the files are located in the location specified in the previous section.

#### Install via gem (Recommended):
1. Navigate to the `scss` folder in the project directory
2. Install the bourbon and neat gems via command line `gem install bourbon && gem install neat`
3. Install bourbon and neat locally using `bourbon install` and `neat install`
4. The `bourbon` and `neat` folders should now be in the `scss` directory

## Building CSS files
To build the style assets, run the following command from the `scss` directory:
`sass --scss site.scss ../css/local.css`

To generate a compressed version of the styles, use the command:
`sass --scss -t compressed site.scss ../css/local.min.css`

This will compile the scss file `style.scss` into css, minify the css, and move it to the css folder. Changes made to the scss file will not be reflected until that command is executed.


## Conventions for Development

### Structure 
The scaffold styles, variables, and other Sass resources are located in the `base` directory and follows the conventions defined by [Bitters](https://github.com/thoughtbot/bitters). The base directory contain styles for all the basic elements used throughout the project and is accessed by importing `base/base` on the main stylesheet.

### Naming
This project follows the [Block-Element-Modifier, or BEM](http://getbem.com/introduction/) methodology for delcaring CSS names and structuring style rules. In general, BEM recommends avoiding nested, global, and compound selectors unless they are reasonablely reusable. Classes use a single hyphen (`-`) for single block class names (e.g. `my-block`), two underlines `__` to indicate children relationships (e.g. `my-block__button`), and two hyphens for modifiers (e.g. `my-block__button--success`).

### Scss Linter
[scss-lint](https://github.com/brigade/scss-lint) is used to help keep the SCSS files clean and readable. The linting rules for this project can be found in the configuration file `.scss-lint.yml` within the `scss` folder.

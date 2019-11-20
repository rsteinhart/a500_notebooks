# bash prompt for macos

put this into your ~/.bash_profile to get aprompt that shows
your git branch and conda environment


parse_git_branch () {

    while read -r branch; do
        [[ $branch = \** ]] && current_branch=${branch#* }
    done < <(git branch 2>/dev/null)

    [[ $current_branch ]] && printf '[%s]' "$current_branch"

}

function condap()
{
    #the_name=$(hostname) -- Linux
    the_name=$(scutil --get LocalHostName)
    out=`basename $CONDA_PREFIX`
    unset PS1
    PS1='\w ${out} $(parse_git_branch) \u@${the_name}\n% '
}


function con()
{
    conda activate $1
    condap
}

#activate the work environment
con work


function get_children(state, size)
    children = String[]

    index = findfirst(".", state)
    index = index[1]

    if (index - 1) > 0 & mod1((index - 1), size) != 0
        push!(children, swap_characters(state, index, index - 1))
    end

    if mod1((index + 1), size) != 0
        push!(children, swap_characters(state, index, index + 1))
    end

    # Swap . with down
    if (index + size) < length(state)
        push!(children, swap_characters(state, index, index + size))
    end

    # Swap . with up
    if (index - size > 0)
        push!(children, swap_characters(state, index, index - size))
    end

    println(children)
end

function swap_characters(state, index1, index2)
    new_state = collect(state)
    temp = new_state[index1]
    new_state[index1] = new_state[index2]
    new_state[index2] = temp
    to_return = ""
    for character in new_state
        to_return = string(to_return, string(character))
    end
    return to_return
end

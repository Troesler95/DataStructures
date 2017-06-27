require 'benchmark'

class Heap
  #use ruby magic to create default getters and setters for instance vars
  attr_accessor :SIZE, :last, :heap

  #logic to perform to initialize the heap
  def initialize(heap_size, example)
    @SIZE = heap_size
    @last = -1
    @heap = Array(@SIZE)

    if example
      success = self._build_heap
    else
      return
    end
    if success
    else
      raise 'Unable to initialize heap. Something went wrong'
    end
  end

  #heap algorithm for inserting data and then heaping up if necessary
  def insert_heap(data)
    #if full, return false
    if @last == @SIZE - 1
      return false
    end

    #increment list size
    @last+=1

    #add data at the end of list
    @heap[@last] = data
    #reheap the heap
    self._reheap_up(@last)
    #return successful
    true
  end

  def delete_heap
    if @last < 0
      return nil
    end

    temp = @heap[0]
    @heap[0] = @heap[@last]
    @last -= 1
    self._reheap_down(0)

    temp
  end

  def print_heap(root=0, level=0)
    if root <= @last
      child = root * 2 + 1
      print_heap(child+1, level+1)

      level.times do
        putc "\t"
      end
      puts "#{@heap[root]}(#{root})"

      self.print_heap(child, level+1)
    end
  end

  def heap_sort
    effective_range = @last

    while effective_range > 0
      __swap_head(effective_range)
      effective_range -= 1
      self._reheap_sort(0, effective_range)
    end

    return @heap
  end

  ###Protected helper methods
  protected
    #initialize heap to half full with random numbers
    def _build_heap
      heap_last = @SIZE / 2 - 1

      heap_last.times do
        num = Random.rand(999) + 1
        if self.insert_heap(num)
          puts "#{num} added to heap."
        else
          puts "Unable to add #{num} to heap"
          return false
        end
      end

      true
    end

    def _reheap_up(index)
      #if not root of heap
      if index > 0
        #store parent node
        parent = (index - 1) / 2

        #if current node is larger than parent
        if @heap[index] > @heap[parent]
          #swap parent and child
          __swap(index, parent)
          #check to see if need to reheap again
          self._reheap_up(parent)
        end
      end
    end

    def _reheap_down(index)
      #if there is a root node
      if (index * 2 + 1) <= @last
        #save index of left child
        key_left = @heap[index * 2 + 1]
        #if there is a right child
        if (index * 2 + 2) <= @last
          key_right = @heap[index * 2 + 2]
        else
          key_right = -1
        end

        #Find larger of the two children
        if key_left > key_right
          key_larger = key_left
          index_larger = index * 2 + 1
        else
          key_larger = key_right
          index_larger = index * 2 + 2
        end

        #test if root is larger than the subtree
        if @heap[index] < key_larger
          ###REPLACE WITH __swap() FUNCTION
          __swap(index, index_larger)

          #see if need reheap
          self._reheap_down(index_larger)
        end
      end
    end

  def _reheap_sort(index, range)
    if (index * 2 + 1) <= range
      #save index of left child
      key_left = @heap[index * 2 + 1]
      #if there is a right child
      if (index * 2 + 2) <= range
        key_right = @heap[index * 2 + 2]
      else
        key_right = -1
      end

      #Find larger of the two children
      if key_left > key_right
        key_larger = key_left
        index_larger = index * 2 + 1
      else
        key_larger = key_right
        index_larger = index * 2 + 2
      end

      #test if root is larger than the subtree
      if @heap[index] < key_larger
        ###REPLACE WITH __swap() FUNCTION
        __swap(index, index_larger)

        #see if need reheap
        self._reheap_sort(index_larger, range)
      end
    end
  end

  private
    #helper function for swapping nodes
    def __swap(index_child, index_parent)
      temp = @heap[index_parent]
      @heap[index_parent] = @heap[index_child]
      @heap[index_child] = temp
    end

    def __swap_head(index_of_last)
      temp = @heap[0]
      @heap[0] = @heap[index_of_last]
      @heap[index_of_last] = temp
    end
end

def heap_sort(arr, arr_size)
  heap = Heap.new(arr_size, false)

  #put each element into a heap
  arr.each{ |n| heap.insert_heap(n)}

  #implement heapsort in the heap class!
  arr = heap.heap_sort
end

def heap_sort_example(arr_size)
  arr = Array.new(arr_size)

  #populate array with random integers between 1 and 1000
  arr_size.times do |n|
    arr[n] = Random.rand(999) + 1
  end

  puts 'Before HeapSort: '
  arr_size.times do |n|
    print("#{arr[n]}, ")
  end
  puts ' '

  arr = heap_sort(arr, arr.size)

  puts 'After HeapSort: '
  arr_size.times do |n|
    print("#{arr[n]}, ")
  end
  puts ' '
end

#from http://sandmoose.com/post/59658391296/quicksort-in-ruby
def quicksort(array)
  return array if array.length <= 1

  pivot_index = (array.length / 2).to_i
  pivot_value = array[pivot_index]
  array.delete_at(pivot_index)

  lesser = Array.new
  greater = Array.new

  array.each do |x|
    if x <= pivot_value
      lesser << x
    else
      greater << x
    end
  end

  return quicksort(lesser) + [pivot_value] + quicksort(greater)
end

# I don't like this as much as you don't...
def bubble_sort(array)
  n = array.size
  begin
    new_n = 0
    for i in (1..n-1)
      if array[i-1] > array[i]
        temp = array[i]
        array[i] = array[i-1]
        array[i-1] = temp
        new_n = i
      end
    end
    n = new_n
  end until n == 0
end

###############################MAIN DEMONSTRATION###########################################################

heap = Heap.new(32, true)
quit = false


begin
  heap.print_heap
  puts 'Please enter an action to perform <I:"insert", D:"delete", Q:"quit">: '
  choice = gets.chomp.upcase

  case choice
    when 'I'
      if heap.SIZE > heap.last
        begin
          puts 'What integer should we insert? (type random for a random number)'
          insert = gets.chomp
          if insert.upcase == 'RANDOM'
            heap.insert_heap(Random.rand(999) + 1)
          else
            insert = Integer(insert)
            heap.insert_heap(insert)
          end

        rescue ArgumentError
            puts "Unable to convert #{insert} to an integer."
            puts "Please be sure to input only numbers with no floating point value."
            retry
        end
      else
        puts "The heap has reached it's cap of #{heap.SIZE}"
      end
    when 'D'
      if heap.last > 0
        temp = heap.delete_heap

        puts "#{temp} removed from heap."
      else
        puts 'There is nothing in the heap! Use the insert function!'
      end
    when 'Q'
      quit = true
    else
      puts 'I didn\'t understand. Please try again!'
  end
end until quit

######################################END MAIN DEMONSTRATION####################################################
######################################HEAP SORT DEMONSTRATION###################################################
heap_sort_example(32)
######################################END HEAP SORT DEMONSTRATION###############################################
######################################BENCHMARK TESTS###########################################################
=begin
size = 1000
test1 = Array.new(size)
test2 = Array.new(size)
test3 = Array.new(size)
#test4 = Array.new(size)

size.times do |x|
  test1[x] = Random.rand(10_000) + 1
  test2[x] = Random.rand(10_000) + 1
  test3[x] = Random.rand(10_000) + 1
  #test4[x] = Random.rand(10_000) + 1
end

puts "Completely random list of #{size} integers (1-10,000):"
Benchmark.bm(14) do |x|
  #x.report('Bubble sort:') {bubble_sort(test4)}
  x.report('Heap Sort:') {heap_sort(test1, size)}
  x.report('Quick Sort:') {quicksort(test2)}
  x.report('Ruby .sort:') {test3.sort}
end
puts ''

(size-50).times do |x|
  test1[x] = x
  test2[x] = x
  test3[x] = x
  #test4[x] = x
end

50.times do |x|
  test1[size-x] = Random.rand(10_000) + 1
  test2[size-x] = Random.rand(10_000) + 1
  test3[size-x] = Random.rand(10_000) + 1
  #test4[size-x] = Random.rand(10_000) + 1
end

puts "Nearly sorted list of #{size} integers (1-10,000):"
Benchmark.bm(14) do |x|
  #x.report('Bubble sort:') {bubble_sort(test4)}
  x.report('Heap Sort:') {heap_sort(test1, size)}
  x.report('Quick Sort:') {quicksort(test2)}
  x.report('Ruby .sort:') {test3.sort}
end
puts ''
puts ''
############################LARGER INTEGERS##################################

size.times do |x|
  test1[x] = Random.rand(1000000) + 1
  test2[x] = Random.rand(1000000) + 1
  test3[x] = Random.rand(1000000) + 1
  #test4[x] = Random.rand(1000000) + 1
end

puts "Completely random list of #{size} integers (1-1M):"
Benchmark.bm(14) do |x|
  #x.report('Bubble sort:') {bubble_sort(test4)}
  x.report('Heap Sort:') {heap_sort(test1, size)}
  x.report('Quick Sort:') {quicksort(test2)}
  x.report('Ruby .sort:') {test3.sort}
end
puts ''

(size-50).times do |x|
  test1[x] = x
  test2[x] = x
  test3[x] = x
  #test4[x] = x
end

50.times do |x|
  test1[size-x] = Random.rand(1000000) + 1
  test2[size-x] = Random.rand(1000000) + 1
  test3[size-x] = Random.rand(1000000) + 1
  #test4[size-x] = Random.rand(1000000) + 1
end

puts "Nearly sorted list of #{size} integers (1-1M):"
Benchmark.bm(14) do |x|
  #x.report('Bubble sort:') {bubble_sort(test4)}
  x.report('Heap Sort:') {heap_sort(test1, size)}
  x.report('Quick Sort:') {quicksort(test2)}
  x.report('Ruby .sort:') {test3.sort}
end
####################################END BENCHMARK TESTS#########################################################
=end
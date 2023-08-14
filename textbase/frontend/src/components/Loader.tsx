import { Bars } from  'react-loader-spinner'

const Loader = () => {
  return (
    <div className="bg-indigo-500 hover:bg-indigo-600 rounded-xl px-5 py-1 flex justify-center items-center">
			<Bars
				height="25"
				width="25"
				color="white"
				ariaLabel="bars-loading"
				wrapperStyle={{}}
				wrapperClass=""
				visible={true}
			/>
    </div>
  )
}

export default Loader
import { FaEdit, FaTrashAlt, FaEye } from 'react-icons/fa';

const AdminTable = ({ 
  columns, 
  data, 
  onEdit, 
  onDelete, 
  onView, 
  isLoading,
  emptyMessage = "Nenhum item encontrado" 
}) => {
  if (isLoading) {
    return (
      <div className="animate-pulse bg-white rounded-lg shadow overflow-hidden">
        <div className="h-12 bg-gray-100 border-b"></div>
        {[...Array(5)].map((_, i) => (
          <div key={i} className="h-16 border-b"></div>
        ))}
      </div>
    );
  }

  if (!data || data.length === 0) {
    return (
      <div className="bg-white rounded-lg shadow p-6 text-center">
        <p className="text-gray-500">{emptyMessage}</p>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-lg shadow overflow-hidden">
      <div className="overflow-x-auto">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              {columns.map((column) => (
                <th
                  key={column.key}
                  className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                >
                  {column.label}
                </th>
              ))}
              <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                Ações
              </th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {data.map((item) => (
              <tr key={item.id} className="hover:bg-gray-50">
                {columns.map((column) => {
                  const value = column.render 
                    ? column.render(item) 
                    : item[column.key];
                    
                  return (
                    <td key={`${item.id}-${column.key}`} className="px-6 py-4 whitespace-nowrap">
                      {value}
                    </td>
                  );
                })}
                <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                  <div className="flex justify-end space-x-2">
                    {onView && (
                      <button
                        onClick={() => onView(item)}
                        className="text-blue-600 hover:text-blue-900"
                        title="Visualizar"
                      >
                        <FaEye />
                      </button>
                    )}
                    {onEdit && (
                      <button
                        onClick={() => onEdit(item)}
                        className="text-blue-600 hover:text-blue-900"
                        title="Editar"
                      >
                        <FaEdit />
                      </button>
                    )}
                    {onDelete && (
                      <button
                        onClick={() => onDelete(item)}
                        className="text-red-600 hover:text-red-900"
                        title="Excluir"
                      >
                        <FaTrashAlt />
                      </button>
                    )}
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default AdminTable;